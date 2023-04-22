from __future__ import annotations

import datetime
from typing import List, Optional

from streamlit.elements.lib.column_config_utils import (
    ColumnConfig,
    ColumnType,
    ColumnWidth,
)


def column_config(
    type: ColumnType | None = None,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: str
    | int
    | float
    | datetime.datetime
    | datetime.date
    | datetime.time
    | None = None,
    min: int
    | str
    | float
    | datetime.datetime
    | datetime.date
    | datetime.time
    | None = None,
    max: int
    | str
    | float
    | datetime.datetime
    | datetime.date
    | datetime.time
    | None = None,
    format: str | None = None,
    step: int | float | None = None,
    validate: str | None = None,
    options: List[str | int | float] | None = None,
    timezone: str | None = None,
) -> ColumnConfig:
    """Configuration options for columns in `st.dataframe` and `st.data_editor`.

    Parameters
    ----------

    type: str
        The display type for the column. Allowed types are "text", "number", "checkbox",
        "select", “list”,“datetime”, “date”, “time”, “url”, “image”, “line_chart”,
        “bar_chart”, “range”. If None, infers the display type from the Pandas data type.
        Defaults to None.
    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        Whether the column should be hidden. Defaults to False.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        If True, a cell can only be submitted by the user if it has a value.
    default:  int, str, float, datetime.datetime, datetime.date, datetime.time, or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    min : int, str, float, datetime.datetime, datetime.date, datetime.time, or None
        The minimum value in a cell. For chart cells, this is the minimum of the y-axis.
        For range cells, this is the minimum of the range bar.
        For number and datetime cells, this is the minimum value that can be inserted.
        For text cells, this is the minimum number of chars. Defaults to None.
    max : int, str, float, datetime.datetime, datetime.date, datetime.time, or None
        The maximum value in a cell. For chart cells, this is the maximum of the y-axis.
        For range cells, this is the maximum of the range bar. For number and datetime
        cells, this is the maximum value that can be inserted. For text cells, this is
        the maximum number of chars. Defaults to None.
    format : str or None
        A format string that specifies how number and datetime cells should be formatted.
        Defaults to None.
    step: int or float or None
        Specifies the value granularity and precision that can be entered by the user.
        This can be used for number, range  or datetime cells.
    validate: str or None
        A regular expression that edited values should be validated against.
        If the input is invalid, it will not be submitted by the user.
    options: list of str or None
        A list of options to choose from. If None, uses the categories from the
        underlying column in case it is configured as dtype "category".
    timezone: str or None
        The timezone applied to datetime columns.
        If None, the timezone is inferred from the Pandas data type. Defaults to None.
    """

    def _format_datetime(
        value: datetime.datetime | datetime.date | datetime.time | None,
    ) -> str | None:
        return None if value is None else value.isoformat()

    if isinstance(default, (datetime.datetime, datetime.date, datetime.time)):
        default = _format_datetime(default)

    if isinstance(min, (datetime.datetime, datetime.date, datetime.time)):
        min = _format_datetime(min)

    if isinstance(max, (datetime.datetime, datetime.date, datetime.time)):
        max = _format_datetime(max)

    min_name = "min_value"
    max_name = "max_value"

    if type == "line_chart" or type == "bar_chart":
        min_name = "y_min"
        max_name = "y_max"

    if type == "text" or type == "url":
        min_name = "min_chars"
        max_name = "max_chars"

    return ColumnConfig(
        type=type,
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=default,
        type_options={
            min_name: min,
            max_name: max,
            "format": format,
            "step": step,
            "validate": validate,
            "options": options,
            "timezone": timezone,
        },
    )


def NumberColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: int | float | None = None,
    min_value: int | float | None = None,
    max_value: int | float | None = None,
    format: str | None = None,
    step: int | float | None = None,
) -> ColumnConfig:
    """Rendering and editing of numerical values.

    When used with `st.data_editor`, editing will be enabled with a numeric input widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        If True, a cell can only be submitted by the user if it has a value.
    default: int or float or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    min_value : int or float or None
        The minimum value that can be entered by the user.
        If None, there will be no minimum.
    max_value : int or float or None
        The maximum value that can be entered by the user.
        If None, there will be no maximum.
    format : str or None
        A printf-style format string controlling how the cell value is displayed.
    step: int or float or None
        Specifies the value granularity and precision that can be entered by the user.
        If None, defaults to 1 for integers. Float numbers will be unrestricted by default.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        type="number",
        default=default,
        type_options={
            "min_value": min_value,
            "max_value": max_value,
            "format": format,
            "step": step,
        },
    )


def TextColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: str | None = None,
    max_chars: int | None = None,
    validate: str | None = None,
) -> ColumnConfig:
    """Rendering and editing of text values.

    When used with `st.data_editor`, editing will be enabled with a text input widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: str or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    max_chars: int or None
        The maximum number of characters that can be entered by the user.
        If None, there will be no maximum.
    validate: str or None
        A regular expression that edited values should be validated against.
        If the input is invalid, it will not be submitted by the user.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=default,
        type="text",
        type_options={
            "max_chars": max_chars,
            "validate": validate,
        },
    )


def UrlColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: str | None = None,
    max_chars: int | None = None,
) -> ColumnConfig:
    """Rendering and editing of clickable URL values.

    When used with `st.data_editor`, editing will be enabled with a text input widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: str or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    max_chars: int or None
        The maximum number of characters that can be entered by the user.
        If None, there will be no maximum.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=default,
        type="url",
        type_options={
            "max_chars": max_chars,
        },
    )


def CheckboxColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: bool | None = None,
) -> ColumnConfig:
    """Rendering and editing of boolean values using checkboxes.

    When used with `st.data_editor`, editing will be enabled with a checkbox widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: bool or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=default,
        type="checkbox",
    )


def SelectColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: str | int | float | None = None,
    options: List[str | int | float] | None = None,
) -> ColumnConfig:
    """Rendering and editing of categorical values using selectboxs.

    When used with st.data_editor, editing will be enabled with a selectbox widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: str or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    options: list of str or None
        A list of options to choose from. If None, uses the categories from the
        underlying column in case it is configured as dtype "category".
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=default,
        type="select",
        type_options={
            "options": options,
        },
    )


def BarChartColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    y_min: int | float | None = None,
    y_max: int | float | None = None,
) -> ColumnConfig:
    """Visualizes a list of numbers in a cell as a bar chart.

    This is a read-only type. It can be used with `st.data_editor`,
    but users will not be able to edit the cell values.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    y_min: int or float or None
        The minimum value of the y-axis of the chart.
        If None, the scales will be normalized individually for each column.
    y_max: int or float or None
        The maximum value of the y-axis of the chart.
        If None, the scales will be normalized individually for each column.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        type="bar_chart",
        type_options={
            "y_min": y_min,
            "y_max": y_max,
        },
    )


def LineChartColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    y_min: int | float | None = None,
    y_max: int | float | None = None,
) -> ColumnConfig:
    """Visualizes a list of numbers in a cell as a line chart.

    This is a read-only type. It can be used with `st.data_editor`,
    but users will not be able to edit the cell values.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    y_min: int or float or None
        The minimum value of the y-axis of the chart.
        If None, the scales will be normalized individually for each column.
    y_max: int or float or None
        The maximum value of the y-axis of the chart.
        If None, the scales will be normalized individually for each column.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        type="line_chart",
        type_options={
            "y_min": y_min,
            "y_max": y_max,
        },
    )


def ImageColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
):
    """Rendering of cell values as images, given valid image URLs or binary data.

    This is a read-only type. It can be used with `st.data_editor`, but users will not
    be able to edit the cell values.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    """
    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        type="image",
    )


def ListColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
):
    """Rendering of list-values as a list of tags.

    This is a read-only type. It can be used with `st.data_editor`,
    but users will not be able to edit the cell values.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    """
    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        type="list",
    )


def DateTimeColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: datetime.datetime | None = None,
    format: str | None = None,
    min_value: datetime.datetime | None = None,
    max_value: datetime.datetime | None = None,
    step: int | float | None = None,
    timezone: str | None = None,
) -> ColumnConfig:
    """Rendering and editing of datetime values.

    When used with `st.data_editor`, editing will be enabled with a datetime picker widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: datetime.datetime or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    format: str or None
        A momentJS-style format string controlling how the cell value is displayed.
    min_value: datetime.datetime or None
        The minimum datetime that can be entered by the user.
        If None, there will be no minimum.
    max_value: datetime.datetime or None
        The maximum datetime that can be entered by the user.
        If None, there will be no maximum.
    timezone: str or None
        The timezone of this column.
    step: int or float or None
        Specifies the value granularity in seconds that can be entered by the user.
        If None, the step will be 1 second.
    """

    # TODO: Check if this code is correct:
    def _format_datetime(value: datetime.datetime | None) -> str | None:
        return None if value is None else value.isoformat()

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=_format_datetime(default),
        type="datetime",
        type_options={
            "format": format,
            "min_value": _format_datetime(min_value),
            "max_value": _format_datetime(max_value),
            "step": step,
            "timezone": timezone,
        },
    )


def TimeColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: datetime.time | None = None,
    format: str | None = None,
    min_value: datetime.time | None = None,
    max_value: datetime.time | None = None,
    step: int | float | None = None,
) -> ColumnConfig:
    """Rendering and editing of time values.

    When used with `st.data_editor`, editing will be enabled with a time picker widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: datetime.time or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    format: str or None
        A momentJS-style format string controlling how the cell value is displayed.
    min_value: datetime.time or None
        The minimum time that can be entered by the user.
        If None, there will be no minimum.
    max_value: datetime.time or None
        The maximum time that can be entered by the user.
        If None, there will be no maximum.
    step: int or float or None
        Specifies the value granularity in seconds that can be entered by the user.
        If None, the step will be 0.1 second.
    """

    # TODO: Check if this code is correct:
    def _format_datetime(value: datetime.time | None) -> str | None:
        return None if value is None else value.isoformat()

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=_format_datetime(default),
        type="time",
        type_options={
            "format": format,
            "min_value": _format_datetime(min_value),
            "max_value": _format_datetime(max_value),
            "step": step,
        },
    )


def DateColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: datetime.date | None = None,
    format: str | None = None,
    min_value: datetime.date | None = None,
    max_value: datetime.date | None = None,
) -> ColumnConfig:
    """Rendering and editing of date values.

    When used with `st.data_editor`, editing will be enabled with a date picker widget.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        An optional boolean, which hides the column if set to True.
        If True, a cell can only be submitted by the user if it has a value.
    default: datetime.date or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    format: str or None
        A momentJS-style format string controlling how the cell value is displayed.
    min_value: datetime.date or None
        The minimum date that can be entered by the user.
        If None, there will be no minimum.
    max_value: datetime.date or None
        The maximum date that can be entered by the user.
        If None, there will be no maximum.
    """

    # TODO: Check if this code is correct:
    def _format_datetime(value: datetime.date | None) -> str | None:
        return None if value is None else value.isoformat()

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        default=_format_datetime(default),
        type="date",
        type_options={
            "format": format,
            "min_value": _format_datetime(min_value),
            "max_value": _format_datetime(max_value),
        },
    )


def RangeColumn(
    *,
    title: str | None = None,
    width: ColumnWidth | None = None,
    hidden: bool | None = None,
    help: str | None = None,
    disabled: bool | None = None,
    required: bool | None = None,
    default: int | float | None = None,
    min_value: int | float | None = None,
    max_value: int | float | None = None,
    format: str | None = None,
) -> ColumnConfig:
    """Visualizes a numeric value using a progress bar-like element.

    This is a read-only type. It can be used with `st.data_editor`,
    but users will not be able to edit the cell values.

    Parameters
    ----------

    title: str
        The title of the column, shown at the top in the column header.
        If None, the column name is used.
    width: "small" or "medium" or "large" or None
        The display width of the column.
        If None, the column will be sized to fit its contents.
    help: str or None
        An optional tooltip that gets displayed when hovering over the column header.
    hidden: bool or None
        An optional boolean, which hides the column if set to True.
    disabled: bool or None
       An optional boolean, which disables the editing if set to True.
    required: bool or None
        If True, a cell can only be submitted by the user if it has a value.
    default: int or float or None
        The default value in a cell when the user adds a new row.
        Defaults to None.
    min_value : int or float or None
        The minimum value of the range bar.
        Defaults to 0.
    max_value : int or float or None
        The maximum value of the range bar.
        Defaults to 1.
    format : str or None
        A printf-style format string controlling how the number next to
        the range bar should be formatted.
    """

    return ColumnConfig(
        title=title,
        width=width,
        hidden=hidden,
        help=help,
        disabled=disabled,
        required=required,
        type="range",
        default=default,
        type_options={
            "min_value": min_value,
            "max_value": max_value,
            "format": format,
        },
    )
