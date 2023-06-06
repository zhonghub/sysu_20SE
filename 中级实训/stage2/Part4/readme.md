### 代码运行方式：

#### 1.ModifiedChameleonCritter

```
javac -classpath .:gridworld.jar ModifiedChameleonCritter/*.java && java -classpath .:gridworld.jar:ModifiedChameleonCritter ModifiedChameleonCritterRunner

```



#### 2.ChameleonKid

```
javac -classpath .:gridworld.jar:ModifiedChameleonCritter  ChameleonKid/*.java && java -classpath .:gridworld.jar:ModifiedChameleonCritter:ChameleonKid ChameleonKidRunner

```



#### 3.RockHound

```
javac -classpath .:gridworld.jar RockHound/*.java  && java -classpath .:gridworld.jar:RockHound RockHoundRunner

```



#### 4.BlusterCritter

```
javac -classpath .:gridworld.jar BlusterCritter/*.java  && java -classpath .:gridworld.jar:BlusterCritter BlusterCritterRunner

```



#### 5.QuickCrab

```
javac -classpath .:gridworld.jar QuickCrab/*.java  && java -classpath .:gridworld.jar:QuickCrab QuickCrabRunner

```



#### 6.KingCrab

```
javac -classpath .:gridworld.jar:QuickCrab KingCrab/*.java  && java -classpath .:gridworld.jar:QuickCrab:KingCrab KingCrabRunner

```

