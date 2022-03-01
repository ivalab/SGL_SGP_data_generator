# SGL_SGP_data_generator
Data generator, based on AI2THOR, is proposed for automatically generate data with ground-truth for symbolic goal learning and scene graph parsing tasks.

## Installation
0. Create a new conda enviroment
```
conda create --name data_gen python=3.6
```
2. Activate created environment
```
conda activate data_gen
```
3. Install requirements
```
pip install -r requirements.txt
```

### Usage
There are five scripts for generating data of picking and placing, object delivery, cutting, cooking and cleaning tasks. Take picking and placing task for example,
you need to first run corresponding task configuration generation. To be noticed, saving_path should be the one for save_root for the later data generation script.
```
python ./script/picknplace_task_json_gen.py path_to_saving_folder
```
Then there are two types of scripts for each task; one is for generating vision-complete scenarios and the other one is for generating vision-incomplete scenarios.
Taking the former one for example,
```
python ./script/picknplace_task_generation.py path_to_saving_folder
```
You could specify the starting and ending index for floorplan, the number of generated data, whether randomize material, whether randomize lighting and etc. 

## License
This Github Repository is released under the MIT License (refer to the LICENSE file for details).

## Citation

If you find this work is helpful and use it in your work, please cite:

```bibtex
@article{xu2022sgl,
  title={SGL: Symbolic Goal Learning for Human Instruction Following in Robot Manipulation},
  author={Xu, Ruinian and Chen, Hongyi and Lin, Yunzhi, and Vela, Patricio A},
  journal={arXiv preprint arXiv:2202.12912},
  year={2022}
}
```
