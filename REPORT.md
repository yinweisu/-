# ECS 171 Final Project Report

### Group Members
1. Weisu Yin, 912105556
2. Hongyi Lyu, 912076326
3. Yue Qiao, 912729725

### Team Name

* 9527

### Command to Generate the Predicted Results


### Description of Final Submitted Model
* We chose to use __Gradient Boosted Decision Tree__ as both the classification model and regression model. When the problem is a classification problem, it is natural to consider __Decision Trees__ because it is a __non-linear__ classifier and it can naturally handle __categorical__ features, which is exactly what we want. 
* However, using only a single __Decision Tree__ is not powerful enough, and it is easy to have over-fitting problem with a single __Decision Tree__. Hence, we would like to combine multiple __Decision Trees__ together to form a more powerful trees: __Random Forest__. With __Random Forest__, we can easily avoid over-fitting and improve our model's stability and accuracy. Neverthless, there is a huge disadvantage of __Random Forest__: its training speed is way too slow. It is very important to have a faster training speed during this project because we have to submit the whole solution online to get the __Eout__, which means we have to run the full dataset during every trial. It is not acceptable to wait several hours between each trial. 
* Therefore, we used __Gradient Boosted Decision Tree__ as our final model. We did not implement the learning algorithm but used the one provided by __SKLEARN__.
```python
clf = GradientBoostingClassifier()
```
* As I mentioned above, training speed is a very important aspect of this project. We noticed that there are many features that are correlated with each other. Knowing this, we are able to pick some features and ignore others. Therefore, we wrote a script to find out the correlation between each features. Examples of our finding are provided below
```
(251, 508, -0.93238698022170152)
(440, 671, -0.32565768355462765)
(502, 509, 1.0)
```
* It turns out that some features are strongly correlated with other features, such as f502 and f509, and some features are only weakly correlated with other features, such as f440 and f671. Weakly correlated features are those that are irreplaceable while strongly correlated features are those somehow having similar attributes. As a result, we tried to find out the top 100 weakly correlated features and top 100 strongly correlated features. 
* Initially, we tried to group features that are strongly correlated together into different sets and only select one feature from each set. Then our learning algorithm would only use the top 100 seakly correlated featrues and features that we selected from different sets. However, the result was not very good. We think this is because we wrongly grouped features together. For example, if f1 and f2 are strongly correlated with a correlation of 0.7; f2 and f3 are strongly correlated with a correlation of 0.7. We group f1, f2 and f3 into a set and select f1 to represent the whole group. However, it is wrong to assume that f1 and f3 are also strongly correlated. 
* As a result, we tried to use both the top 100 weakly correlated features and 100 strongly correlated features. It turns out the result is very promising.