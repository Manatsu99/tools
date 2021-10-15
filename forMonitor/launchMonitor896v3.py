# -*- coding: utf-8 -*-
# 2021/10/07
import configparser
from re import sub
import utils.loggingTool as lTool

import datetime
tz = datetime.timezone(datetime.timedelta(hours=9))
startTime = datetime.datetime.now(tz)

cParser = configparser.ConfigParser()

_sec1 = 'profile_name'
_sec2 = 'version'
_sec3 = 'resources'
_sec4 = 'path'
_sec5 = 'params'
_sec6 = 'callbacks'
_sec7 = 'savefiles'
_sec8 = 'seed'
_sec9 = 'monitorcfg'

def run(profile, test, debug):
    print(type(startTime))
    l = lTool.loggingTool(True,True,True, profile, startTime)
    t = ''
    import sys
    for arg in sys.argv:
        t += arg+' '
    l.i('command: '+t)
    l.i("doing \'run\'")
    l.d("  run.profile: "+str(profile))
    l.d("  run.test: "+str(test))
    l.d("  run.debug: "+str(debug))
    cParser.read(profile)

    l.i("reading profile...")
    c_pName = cParser.get(_sec1, 'name')
    c_version = cParser.getboolean(_sec2, 'train_val_test')
    c_imageSet = cParser.get(_sec3, 'imageset')
    c_root = cParser.get(_sec4, 'root')
    c_ResNet = cParser.get(_sec4, 'ResNet_tf2')
    c_products = cParser.get(_sec4, 'products')
    c_script = cParser.get(_sec4, 'script')
    c_logs = cParser.get(_sec4, 'logs')
    c_text = cParser.get(_sec4, 'text')
    l.dt(c_pName)
    l.dt(c_version)
    l.dt(c_imageSet)
    l.dt(c_root)
    l.dt(c_ResNet)
    l.dt(c_products)
    l.dt(c_script)
    l.dt(c_logs)
    l.dt(c_text)

    identifier = startTime.strftime('%Y%m%d%H%M%S')+ c_pName
    scriptPath = c_root+c_ResNet+c_script
    
    generateConfig(l, cParser, identifier, scriptPath)

    cFileName = identifier+'.ini'

    c_val = cParser.get(_sec9, 'val')
    c_all = cParser.getboolean(_sec9, 'all')
    c_monitor = cParser.get(_sec9, 'scriptname')

    cwd = c_root+c_ResNet+c_script
    textpath = '../../'+c_text
    l.it("c_all: "+str(c_all))
    if c_all is False:
        l.it("WithMonitor")
        communicateWithMonitor(profile, l,c_monitor,  c_val, cFileName, identifier, cwd, textpath, c_imageSet)
    else:
        l.it("WithALL")
        communicateAll(profile, l,c_monitor,  c_val, cFileName, identifier, cwd, textpath, c_imageSet)

def communicateAll(profile, l, monitor, val, conf, identify, _cwd, txtpath, imgset):
    l.i("communicateAll")
    import datetime
    _tz = datetime.timezone(datetime.timedelta(hours=9))
    _startTime = datetime.datetime.now(_tz)
    _l = lTool.loggingTool(True,True,True, profile=profile, startTime=_startTime, name = 'communicateALL')
    import os
    total = sum(os.path.isfile(os.path.join(_cwd+txtpath+imgset, name)) for name in os.listdir(_cwd+txtpath+imgset))
    _l.i("monitor: "+str(monitor))
    _l.i("val: "+str(val))
    _l.i("conf: "+str(conf))
    _l.i("identify: "+str(identify))
    _l.i("Files: "+str(total))

    pass

def communicateWithMonitor(profile, l, monitor, val, conf, identify, _cwd, txtpath, imgset):
    l.i("communicateSubprocess")
    l.d('cwd: '+_cwd)
    l.d('txtpath: '+_cwd+txtpath)
    # getVal
    val = txtpath+imgset+'/'+imgset+'_master_'+val+'.txt'

    # cmd = "python3 "+monitor+" "+val+" "+conf+" -d "+ datetime
    cmd = ['python3', monitor, val, conf, "-d", identify]
    #cmd = 'ls'
    import datetime
    _tz = datetime.timezone(datetime.timedelta(hours=9))
    _startTime = datetime.datetime.now(_tz)
    l.i("cmd: "+str(cmd))
    print(type(_startTime))
    _l = lTool.loggingTool(True,True,True, profile=profile, startTime=_startTime, name = monitor.rsplit('.')[0])
    import subprocess
    p = subprocess.Popen(cmd, cwd=_cwd, 
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT
                       )
    for line in iter(p.stdout.readline, b''):
        _l.i(line.decode('utf-8'))
    p.wait()
    l.i("communicate finished.")

def generateConfig(l, cParser, identifier, scriptPath):
    l.i("reading config from profile...")
    train_bs = cParser.getint(_sec5, 'train_bs')
    test_bs = cParser.getint(_sec5, 'test_bs') 
    nb_epoch = cParser.getint(_sec5, 'nb_epoch') 
    workers = cParser.getint(_sec5, 'workers') 
    max_queue_size = cParser.getint(_sec5, 'max_queue_size') 
    img_rows = cParser.getint(_sec5, 'img_rows') 
    img_cols = cParser.getint(_sec5, 'img_cols') 
    img_channels = cParser.getint(_sec5, 'img_channels') 
    data_augmentation = cParser.getboolean(_sec5, 'data_augmentation')
    nb_classes = cParser.getint(_sec5, 'nb_classes')
    loss_function = 'binary_crossentropy' if nb_classes == 2 else 'categorical_crossentropy'
    network = cParser.get(_sec5, 'network')
    lr = cParser.getfloat(_sec5, 'lr') 
    optimizer = cParser.get(_sec5, 'optimizer') 
    gpu_serial = cParser.get(_sec5, 'gpu_serial') 
    use_lr_reducer = cParser.getboolean(_sec6, 'lr_reducer')
    use_early_stopper = cParser.getboolean(_sec6, 'early_stopper')
    use_model_checkpoint = cParser.getboolean(_sec6, 'model_checkpoint')
    savefiles = (cParser.get(_sec7, i) for i in cParser.options(_sec7))
    rseed = cParser.getint('seed', 'rseed')
    l.dt('train_bs: '+str(train_bs))
    l.dt('test_bs: '+str(test_bs))
    l.dt('nb_epoch: '+str(nb_epoch))
    l.dt('workers: '+str(workers))
    l.dt('max_queue_size: '+str(max_queue_size))
    l.dt('img_rows: '+str(img_rows))
    l.dt('img_cols: '+str(img_cols))
    l.dt('img_channels: '+str(img_channels))
    l.dt('data_augmentation: '+str(data_augmentation))
    l.dt('loss_function: '+str(loss_function))
    l.dt('network: '+str(network))
    l.dt('lr: '+str(lr))
    l.dt('optimizer: '+str(optimizer))
    l.dt('gpu_serial: '+str(gpu_serial))
    l.dt('use_lr_reducer: '+str(use_lr_reducer))
    l.dt('use_early_stopper: '+str(use_early_stopper))
    l.dt('use_model_checkpoint: '+str(use_model_checkpoint))
    l.dt('savefiles: ')
    for i in savefiles:
        l.dt('\t'+i)
    l.i("generate config")
    cFileName = identifier+'.ini'
    l.i("config filename: "+cFileName)
    l.i("writing...")
    f = open(scriptPath+cFileName, 'x', encoding='UTF-8')
    writeln(f, '[params]')
    writeln(f, 'train_bs = '+str(train_bs))
    writeln(f, 'test_bs = '+str(test_bs))
    writeln(f, 'nb_epoch = '+str(nb_epoch))
    writeln(f, 'workers = '+str(workers))
    writeln(f, 'max_queue_size = '+str(max_queue_size))
    writeln(f, 'img_rows = '+str(img_rows))
    writeln(f, 'img_cols = '+str(img_cols))
    writeln(f, 'img_channels = '+str(img_channels))
    writeln(f, 'data_augmentation = '+str(data_augmentation))
    writeln(f, 'nb_classes = '+str(nb_classes))
    writeln(f, 'network = '+str(network))
    writeln(f, 'lr = '+str(lr))
    writeln(f, 'optimizer = '+str(optimizer))
    writeln(f, 'gpu_serial = '+str(gpu_serial))
    writeln(f,'')
    writeln(f, '[callbacks]')
    writeln(f, 'lr_reducer = '+str(use_lr_reducer))
    writeln(f, 'early_stopper = '+str(use_early_stopper))
    writeln(f, 'model_checkpoint = '+str(use_model_checkpoint))
    writeln(f,'')
    writeln(f, '[savefiles]')
    savefiles = (cParser.get(_sec7, i) for i in cParser.options(_sec7))
    _i = 1
    for item in savefiles:
        writeln(f, 'item'+str(_i)+' = '+item)
        _i += 1
    writeln(f,'')
    writeln(f, '[savelocate]')
    writeln(f, 'root = '+str('../products'))
    writeln(f,'[seed]')
    writeln(f, 'rseed = '+str(rseed))
    
    f.close()
    l.i("config file saved at "+scriptPath+cFileName)

def writeln(f, message):
    f.write(str(message)+'\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Launch monitor896.py with premade profiles.')
    parser.add_argument('profile', help='Path of the launch profile.')
    parser.add_argument('--test', '-t', help='Add the letters \"test\" to the end of products.', action='store_true')
    parser.add_argument('--debug', '-d', help='For debug this script', action='store_true')
    args = parser.parse_args()
    run(args.profile, args.test, args.debug)