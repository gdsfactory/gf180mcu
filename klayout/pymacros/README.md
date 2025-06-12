# Klayout GUI PCells implementation.

Note: This is not the recommended way to use the GF180MCU PDK. This is a collection of PCells for the GF180MCU PDK inside the KLayout GUI, which is not a supported flow for this PDK.
We strongly recommend using the PDK as a standalone python package, which is available at: `pip install gf180mcu`


If you still want to proceed with this. You could use those PCells either in 2 ways:
1. Use volare built PDK directly from: https://github.com/efabless/volare
2. Use the PDK from this primitive library for testing purposes.

## Using PCells from Volare
Please refer to Volare documentation at: https://github.com/efabless/volare/blob/main/Readme.md

## Using PCells from this repo directly.
To use the PDK from this repo directly, you need to do the following:
1. Go to following folder in the repo `cells/klayout` and then run the following command:
```bash
export KLAYOUT_HOME=`pwd`
```
2.(optional step to enable GUI menu for running DRC/LVS) You will need to run the following commands as well from inside `cells/klayout` folder:
```bash
ln -s ../../rules/klayout/drc
ln -s ../../rules/klayout/lvs
ln -s ../../rules/klayout/macros
ln -s ../../tech/klayout/gf180mcu.lyt
ln -s ../../tech/klayout/gf180mcu.lyp
```
3. Go to any location where you want to start designing, and open klayout using the following command:
```bash
klayout -e
```
4. Create a new layout for testing.
5. Press on insert instance.
6. Go to the instance menu and select "GF180MCU" library from the library list.
7. Select the search button and it will give the list of PCells that is available in the library.
8. Select any cell and it will show the cell.
9. Go to the PCell tap and change the parameters as needed to change the layout of the PCells.
