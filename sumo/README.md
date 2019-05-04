# SUMO urban simulator configuration

[Install SUMO](http://sumo.sourceforge.net/) and make sure to add SUMO to your path (required for certain scripts):

```
export SUMO_HOME="/usr/local/opt/sumo/share/sumo"
```

## Running simulations with SUMO


**GRID simulation** 

```
sumo -c grid.sumocfg
```

## Running simulations with GUI!

Just replace `sumo` with `sumo-gui`

## Creating Additional Maps with SUMO

This step shouldn't be required unless you want to try out new (road) network architectures.

### Create a simulation network (e.g. grid)

```
netgenerate --grid -o grid.net.xml --grid.number 10 --default.lanenumber 1
```


### Create a network from Open Street Maps

Click the export button [open street maps](https://www.openstreetmap.org/) which will be named `map.osm`. 
Convert this into a network file with:

```
netconvert --osm-files map.osm -o your-net-name.net.xml
```

### Create random vehicle routes for `***.net.xml` 

`python /usr/local/opt/sumo/share/sumo/tools/randomTrips.py -n grid.net.xml -r grid.rou.xml -e 1000 -l`

Where 5000 is the number of random vehicles or random routes to create.
 
### Saving new configuration files

Sumo can automatically create configuration files (`***.sumocfg`) based on flags passed to the `sumo` command. Save them with the following:

```
sumo -c your-original-net.sumocfg --some-new-parameter -C your-new-net.sumocfg
```

Of course, in the above, the `.sumcfg` file can (and should) be the same after both the `-c` flag and the `-C` flag.
The distintion of `original` vs `new` is simply to explain the difference between the two flags.
