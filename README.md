# Dagster Demo
Dagster is an orchestrator that's designed for developing and maintaining data assets, such as tables, data sets, machine learning models, and reports.

This is a demo of Dagster basic functionality to understand how it uses assets. We define an asset that is a csv of different brands of breakfast cereals along with a rating of its protein content. We build out assets and graphs off of this dataset, resulting in a more complex lineage graph where we can determine just the Nabisco cereals as well as which of those has the highest protein content.

![image](https://user-images.githubusercontent.com/40530465/204061632-9fd63ad6-8794-4c8a-8c99-f369eeee1a96.png)

![image](https://user-images.githubusercontent.com/40530465/204061140-da23973b-d677-4c22-a776-bda2048f89b6.png)

The tutorial can be found at https://docs.dagster.io/tutorial

## Setup
```
git clone https://github.com/jpolkdata/dagster_demo
cd dagster_demo
python3 /venv/bin/activate
```

## Materializing the Assets
Build out just the list of cereals as an asset from the csv
```
dagit -f cereal.py
```
![image](https://user-images.githubusercontent.com/40530465/204061250-6f71ddd3-03eb-41ce-a6dd-b366ac40b641.png)

Get each cereal's protein content as a fraction, determine just the Nabisco cereals, and then join that data back together to determine the highest protein Nabisco cereal
```
dagit -f serial_asset_graph.py
```
![image](https://user-images.githubusercontent.com/40530465/204061507-bbaa4545-20d4-4b15-9a8b-86bf08c8fcac.png)

In an even more complex example, we instead pull in a zip file containing a separate csv file that contains cereal ratings. We then use that data in calculating the highest protein Nabisco cereal
```
dagit -f complex_asset_graph.py
```
![image](https://user-images.githubusercontent.com/40530465/204061961-a42918c1-d1c2-4b0e-9187-48995d2c2aef.png)



