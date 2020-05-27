# import-todoist.nvim

This is a very simple Neovim plugin to import completed tasks for a given date from Todoist into a
buffer.

This plugin is not created by, affiliated with, or supported by Doist.

## Installation

You will need Neovim, the Neovim Python 3 remote plugin host, and the [Todoist Python API
  module](https://github.com/doist/todoist-python), as well as
  [`dateutil`](https://github.com/dateutil/dateutil/).

Install these dependencies and use your favorite plugin manager to install this plugin. With
[`vim-packager`](https://github.com/kristijanhusak/vim-packager), this looks like:
```vim
call packager#add('wbthomason/import-todoist.nvim')
```

## Usage
This plugin provides the command `TodoistImportCompleted <date>`, which imports completed tasks for the given
date (if the date is not specified, the current date is assumed). If you run it in a buffer which
already has some of your tasks (as detected by `g:todoist_tasks_start_marker`, described below), it
will update your tasks.

## Configuration

`TodoistImportCompleted` inserts completed tasks according to the following configuration variables:

- `g:todoist_format`: the format for each task. Should be a Python 3 format string, where the
  acceptable keys are:
  - `content`: the content of the task (i.e. its text)
  - `project`: the name of the project the task was assigned to
  - `completed`: the full date and time at which the task was completed
  - `completed_time`, `completed_date`: just the time and just the date at which the task was
    completed, respectively.

  Additional keys can be added upon request, from the set listed here: https://developer.todoist.com/sync/v8/?python#items

  I use the following setting:
  ```python
  '- ( ***{project}***: {completed_time} ): {content}'
  ```
- `g:todoist_tasks_start_marker`: the pattern/string marking the start of where you want your tasks
  inserted. Used to find the start of the region to update. I use `## Todoist Tasks`.
- `g:todoist_tasks_end_marker`: the (optional) pattern/string marking the end of where you want your
  tasks inserted. Used to find the end of the region to update. If unset, lines until the end of the
  file will be replaced on an update.
- `g:todoist_token`: your Todoist API token. **DO NOT MAKE THE FILE WHICH SETS THIS VARIABLE
  PUBLIC**.
  - Should this be set via a variable in a file you source during Neovim startup? Probably not; it
    should probably come from an environment variable or similar. If you feel strongly about this,
    let me know.
