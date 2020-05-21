import pynvim
import todoist
from dateutil.parser import parse
from datetime import datetime
from dateutil.relativedelta import relativedelta


@pynvim.plugin
class TodoistImport:

  def __init__(self, nvim):
    self.nvim = nvim
    token = self.nvim.api.get_var('todoist_token')
    self.api = todoist.TodoistAPI(token)

  @pynvim.function('_todoist_import_completed_for_date')
  def import_completed_for_date(self, target_date):
    if type(target_date) is str:
      target_date = parse(target_date, default=datetime.max)
    since = (target_date - relativedelta(days=+1))
    until = (target_date + relativedelta(days=+1))
    completions = self.api.completed.get_all(until=until.isoformat(), since=target_date.isoformat())

    items = completions['items']
    projects = completions['projects']
    result = []
    format_str = self.nvim.api.get_var('todoist_format')
    for item in items:
      content = item['content']
      project_name = projects[str(item['project_id'])]['name']
      completed = parse(item['completed_date']).astimezone()
      result.append(
          format_str.format(
              content=content,
              project=project_name,
              completed=completed,
              completed_time=completed.time(),
              completed_date=completed.date()
          )
      )

    return result

  @pynvim.command('TodoistImportCompleted', nargs='?')
  def import_completed_cmd(self, args):
    if not args:
      target_date = datetime.now()
    else:
      target_date = parse(args[0], default=datetime.max)

    completed_items = self.import_completed_for_date(target_date)
    tasks_start_marker = self.nvim.api.get_var('todoist_tasks_start_marker')
    try:
      tasks_end_marker = self.nvim.api.get_var('todoist_tasks_end_marker')
    except pynvim.api.common.NvimError:
      tasks_end_marker = None

    tasks_start = self.nvim.funcs.search(tasks_start_marker, 'csw')
    if tasks_start == 0 and self.nvim.current.buffer.api.line_count() > 0:
      tasks_start = -1
      completed_items.insert(0, tasks_start_marker)

    if tasks_end_marker is not None:
      tasks_end = self.nvim.funcs.search(tasks_end_marker, 'cw')
      tasks_end -= 1
      if tasks_end < tasks_start:
        tasks_end = -1
    else:
      tasks_end = -1

    buf = self.nvim.current.buffer
    buf.api.set_lines(tasks_start, tasks_end, False, completed_items)
