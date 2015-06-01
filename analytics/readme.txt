Cleaned up version of visualization code, restructured to make it a little easier to
produce JSON for javascript charting.. Some notes:

Manifest:
  Code:
      lives in energy/energy_views.py
        executing energy.py at the command line produces PNG files in the folder ../figs
  Data:
      the file data/Temprature.csv is required (could move into the API)
      the code caches a local copy of the energy data in data/Energy.json (mostly
      so I could work while a guest of NJT)

Usage:
  views = EnergyViews('http://slacker87.koding.io:3000/api/raw', force=True)

      - force=True forces an API fetch

  plots = views.plots(
      what,                   - 'gas' or 'pwr'
      'PRINCETON TWP',        - or 'PRINCETON BORO'
      business_class,         - a string ('Residential' etc.) or a list of strings
      per_meter,              - False => aggregate plots, True => divide by # meters
      scale)                  - for scaling to larger/smaller units

      - when business_class is a list, the named timeseries are summed up
      - returns a dictionary with data for 4 plots:
        a) ln_time: data
           pandas Series indexed by time. Convert to a vector pair or point sequence as:
                  (data.index.values, data.values)
              or  zip(data.index.values, data.values)
        b) ln_cool: (cool, line)
        c) ln_warm: (warm, line)
           x and y points on a straight line corresponding to tempratures during cool
           months (=heating data) or warm months (=cooling data for power, baseload for
           gas). Convert to a vector pair or point sequence as:
                  (cool.values, line.values)
              or  zip(cool.values, line.values)
        d) scatter: (temp, data)
           x and y points for a scatter plot of consumption vs temprature. Convert to a
           vector pair or point sequence as:
                  (temp.values, data.values)
              or  zip(temp.values, data.values)
        current outputs were in pandas datatypes because I wanted to be lazy and use the
        pandas plotting API for some bits

  fig1 = draw_quad(views, 'gas', 'Gas', 'Therms', 1.0, Residential')
      - function draws a couple of plots and is an illustration of use (mostly only
        if you are using matplotlib)

To do:
- smooth the spikes from estimated billing
- normalize for heating/cooling degree days
- use that to show how much energy is used for heating, cooling and how much is baseload
- use approximate cost to show how much ($, %) is spent on heating, cooling etc.
- if we can get some residents to show their billing, they can compare themselves to the
  Joneses

