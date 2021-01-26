# 一站式讲明白Mockito打桩测试常用的几个接口
本文不求讲的全面，只求讲的实用，拿来就能用。另外本文没有涉及到异常相关的打桩，下次再续。

## 1. 几个术语：

真实对象：代码中定义的class，并使用new方法初始化的对象

mock对象：模拟真实对象的对象，采用Mockito初始化的对象

真实方法：class中定义的方法

mock方法：采用Mockito定义的方法，测试时用来替代真实方法

## 2. Mock对象和Mock部分对象(partial-mock)
### 场景
Mock对象的场景是：测试过程中，对于某些不容易构造或者不容易获取的对象，就可以用一个虚拟的对象来创建以便测试。
Mock部分对象的场景：希望调用部分mock的方法，其余的方法调用真实的方法。

### 接口

```java
// mock整个对象，对函数掉调用都使用mock的方法，除非显示的调用doCallRealMethod()
Mockito.mock(Class<T> classToMock, MockSettings mockSettings) 
//mock部分对象，对函数的调用均执行真正的方法，除了使用doXxx或者thenXxx的部分。
Mockito.spy(Class<T> classToSpy)
```
### 实例
```java
// 默认就执行mock方法
JobManager jobManager = Mockito.mock(JobManager.class);
// 除了在测试用例中打桩mock的方法以外，其他都执行真实的方法
JobManager jobManager = Mockito.spy(JobManager.class);
```

## 3. 否真正执行方法，doXxx和thenXxx
### 场景
1. doXxx的接口都是不会执行对象的真实方法，直接执行doXxx中的方法/值/异常。
2. thenXxx的接口都是会先执行对象的真实方法，然后返回thenXxx中的处理逻辑/值/异常。
### 接口
```java
Mockito.doReturn(Object toBeReturned)
Mockito.doAnswer(Answer answer)
Mockito.doThrow(Throwable... toBeThrown)
......
thenReturn(T var1)
thenAnswer(Answer<?> var1)
thenThrow(Throwable... var1)
......
```

### 实例
```java
// doXxx公式：doXxx(返回值/方法).when(mock对象).对象的方法(入参的类型)，
// doXxx如果没有逻辑也可以doNothing，例如：
Mockito.doReturn(response).when(jobManager).queryUser(any(User.class));
// thenXxx公式：when(mock对象.方法).thenXxx(返回值/逻辑)，例如
Mockito.when(jobManager.queryUser(any(User.class))).thenReturn(user1);
```

## 4. Mock方法的返回值，doReturn 和 thenReturn
### 场景
doReturn或者thenReturn一般是直接给一个方法的返回值（不是一段代码逻辑）。
### 接口
```java
Mockito.doReturn(Object toBeReturned)
Mockito.doReturn(Object toBeReturned, Object... toBeReturnedNext)
thenReturn(T var1);
thenReturn(T var1, T... var2);
```
### 实例
```java
// 调用jobManager的queryUser方法时，不论入参是多少，直接返回"user0"
Mockito.doReturn("user0").when(jobManager).queryUser(any(User.class));
// 调用jobManager的queryUser方法时，正常调用该类的真实方法
Mockito.when(jobManager.queryUser(any(User.class))).thenReturn("user0");

// doReturn 和thenReturn可以支持按照调用次数返回多个不同的值，比如第一次调用返回user0，第二次返回user1，如下：
Mockito.doReturn("user0"，"user1", "user2").when(jobManager).queryUser(any(User.class));
Mockito.when(jobManager.queryUser(any(User.class))).thenReturn("user0"，"user1", "user2");
```
## 5. Mock方法，根据不同入参返回不同处理逻辑，thenAnswer和doAnswer
### 场景
某些方法没有一个固定的返回值，需要根据入参的具体参数值，执行一些代码逻辑就用thenAnswer或者doAnswer。
同样，使用doAnswer的接口都是不会执行对象的真实方法，直接执行doAnswer的定义的方法。
使用thenAnswer的接口会先执行真实方法，然后调用thenAnswer中定义的方法进行返回。

### 接口
```java 
Mockito.doAnswer(Answer answer)
thenAnswer(Answer<?> var1)
```

### 实例
mock一个根据userId获取firstTask的方法，假设真实方法是去数据库中查询，那么此处就可以根据userId直接返回一个task对象。
```java
Map<String, UserInfo> userInfos=new HashMap<>();
Map<String, TaskInfo> taskInfos = new HashMap<>();
......
Mockito.doAnswer(new Answer() {
    @Override
    public Object answer(InvocationOnMock invocation) throws Throwable {
        // 只有一个参数
        String userId = invocation.getArgument(0);
        LOGGER.info("userId:" + userId);
        UserInfo userInfo = userInfos.get(userId);
        String userName = userInfo.getName();
        List<TaskInfo> firstTaskInfos = new ArrayList<>();
        TaskInfo taskInfo;
        switch (userName) {
            case "case1":
                taskInfo = taskInfos.get("case1");
                break;
            case "case2":
                taskInfo = taskInfos.get("case2");
                break;
            case "case3":
                taskInfo = taskInfos.get("case3");
                break;
            default:
                throw new IllegalStateException("Unexpected value: " + userName);
        }
        firstTaskInfos.add(taskInfo);
        return beginTaskInfos;
    }
}).when(taskInfoService).getfirstTaskInfosByuserId(anyString());
```
对于thenAnswer中的Answer实现方法和doAnswer是类似的，和doAnswer的区别仍然是doAnswer不需要执行真实方法，直接执行mock方法。thenAnswer是先执行真实方法，然后再执行Answer中定义的方法。



## 6. 设置Mock的对象的属性
### 场景
我遇到的场景是在spring框架下，设置Mock对象不会自动初始化@AutoWired的属性，此时就需要显式的设置Mock对象中需要用到的属性。 其原理是用反射机制来设置的。
### 接口和实例

spring框架中使用如下接口，此方法可以用来设置private的属性：

```java
ReflectionTestUtils.setField(Object targetObject, String name, @Nullable Object value) 
```

或者

```java
Field field = ReflectionUtils.findField(targetClass, name, type);
if (field == null) {
    ....
    }
ReflectionUtils.makeAccessible(field);
ReflectionUtils.setField(field, targetObject, value);
```

如果是非spring框架，也可以直接使用Java的反射机制：
```java
import java.lang.reflect.Field;
......
Field field = target.getClass().getDeclaredField(fieldName);
field.setAccessible(true); //改成可访问，不管现有修饰
field.set(target, value);
```

### 实例

参考资料：
1. https://www.journaldev.com/21816/mockito-tutorial
2. Mockito源码
