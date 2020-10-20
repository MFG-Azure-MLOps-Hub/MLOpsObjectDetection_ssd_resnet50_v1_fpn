
## run train.py

* The model use *ssd_resnet50_v1_fpn_640x640_coco17_tpu-8* as pre-trained-model, if use different model, you need a new pipe.config and change the model_name in train,py.


* The train.py need call "protoc" which is os dependent. only the wind32 version is tested, for linux, please check if the code below is runnable.
```


    elif os_name is 'Linux':
        st = os.stat('../../protoc/protoc-3.13.0-linux-x86_64/bin/protoc')
        os.chmod('../../protoc/protoc-3.13.0-linux-x86_64/bin/protoc', st.st_mode | stat.S_IEXEC)
        subprocess.call(["../../protoc/protoc-3.13.0-linux-x86_64/bin/protoc", "object_detection/protos/*.proto", "--python_out=."])

```

* it will generate 3 folders
1. _my_model - training folder
2. _exported-models -  result folder
3. _pre-trained-models - the pre-trained-model will be download and copy to here


* now the training step is 200 for testing purpose