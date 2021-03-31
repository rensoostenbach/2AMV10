import dash_core_components as dcc
import dash_bootstrap_components as dbc


def OptionMenu(values, label, **kwargs):
    options = [{"label": s.replace("_", " ").capitalize(), "value": s} for s in values]
    kwargs["value"] = kwargs.get("value", values[0])

    if len(options) <= 4:
        component = dbc.RadioItems
        kwargs["inline"] = True
    else:
        component = dbc.Select

    return dbc.FormGroup([dbc.Label(label), component(options=options, **kwargs)])


def CustomRangeSlider(values, label, **kwargs):
    values = sorted(values)
    marks = {i: f"{i // 1000}k" for i in values}

    return dbc.FormGroup(
        [
            dbc.Label(label),
            dcc.RangeSlider(
                min=values[0],
                max=values[-1],
                step=1000,
                value=[values[1], values[-2]],
                marks=marks,
                **kwargs,
            ),
        ]
    )
