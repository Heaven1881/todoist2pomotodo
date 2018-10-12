# todoist2pomotodo
这个工具可以根据Todoist上当日的待办清单以番茄的方式同步到Pomotodo(番茄土豆)上，具体来说，它执行以下内容：
- 登录Todoist，并同步当日或者已过期的待办
- 根据待办的树状结构，将待办拍扁为水平结构
- 登录Pomotodo，添加处理后的待办任务

例如，假设在Todoist中你有如下的任务结构：
 - ProjectA
   - Task1
   - Task2
     - Step1
     - Step2
     
经过处理后，这些任务会被拍扁成：
- #ProjectA Task1
- #ProjectA Task2
- #ProjectA Task2 | Step1
- #ProjectA Task2 | Step2

# 安装
本工具使用`python`编写，因此，确保你拥有运行python脚本的环境。

本工具使用了[request库](https://github.com/requests/requests)来处理HTTP访问，因此在使用工具前，确保request库已经被安装并且可以正常使用。


# 使用方法
编辑config.ini文件，在以下配置中写入两个应用的token
```
[todoist]
token=your token here

[pomotodo]
token=your token here
```

使用如下命令运行脚本即可：

```
python main.py
```

默认情况下，只会将优先级不为0的待办添加到Pomotodo中，如果你希望添加
