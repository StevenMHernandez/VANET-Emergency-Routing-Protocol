Within your ns-3 instance's `./src` directory, clone the repositories:

```
cd src
git clone https://github.com/StevenMHernandez/VANET-Emergency-Routing-Protocol.git
git clone https://gitlab.com/tomhend/modules/epidemic-routing.git
cd ../
```

```
./waf configure --enable-examples
```

```
./waf --run urban-routing-example
```