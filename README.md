## Python run-time type checking utility

Author: [Yuxuan Zhang](mailto:python@z-yx.cc) | [GitHub Repository](https://github.com/zhangyx1998/rttc)

The `rttc` project originates from this [post](https://discuss.python.org/t/runtime-type-checking-using-parameterized-types/70173) on the python discussion forum.

### Usage

#### Want to do something like this?

```python
>>> isinstance(["hello type check"], list[str])
TypeError: isinstance() argument 2 cannot be a parameterized generic
```

#### Just drop-in replace `isinstance()` with `type_check()`

```python
from type_check import type_check

type_check(["hello type check"], list[str]) # True
type_check([1], list[str]) # False
```

And of course you can use type variables!

```
DataType = list[tuple[float, str]]

type_check([(1.0, "hello rttc")], DataType) # True
type_check([(1, 2), [3.0, "4"]] , DataType) # False
```

#### Wondering how far you can go?

These features all work recursively with each other!

- **Union types** are supported:

    ```python
    type_check(1   , int | bool) # True
    type_check(True, int | bool) # True
    type_check("1" , int | bool) # False
    ```

- **Literals** are supported:

    ```python
    type_check("alex", Literal["alex", "bob"]) # True
    type_check("hack", Literal["alex", "bob"]) # False
    ```

- **Inherited classes** are supported:

    ```python
    class C(list[int]):
        pass

    type_check(C([1])  , C) # True
    type_check(C([1.0]), C) # False
    ```

- **Type-hinted classes** are supported:

    ```python
    from typing import TypeVar, Generic, Literal
    from dataclasses import dataclass

    T = TypeVar("T")
    P = TypeVar("P")

    @dataclass
    class C(Generic[T, P]):
        x: T
        y: P
        z: Literal[1]

    type_check(C(x=1  , y="y", z=1), C[int, str]) # True
    type_check(C(x=1.0, y="y", z=1), C[int, str]) # False - C.x = float(1.0) is not int
    type_check(C(x=1  , y="y", z=2), C[int, str]) # False - C.z = int(2) is not Literal[1]
    ```


- **Custom checking hooks**:

    Examples coming soon...

    For now, please refer to [builtin_checks.py](type_check/builtin_checks.py).

### Other tools in the box

#### `type_assert()`

Similar to type_check(), but it raises `TypeCheckError` instead of returns `bool`.
The raised `TypeCheckError` contains debug-friendly information indicating what caused type check to fail (check below for details).

### `type_guard`

This decorator allows you to convert a class or a function into a type-guarded object.
It is analogous to performing a `type_assert` on function return values or on returned class instances.

```python
from type_check import type_guard

@type_guard
def fn(x) -> int | float | str:
    return x

fn(1) # ok

fn([]) # TypeCheckError: list([]) is not int | float | str

from dataclasses import dataclass

@type_guard
@dataclass
class C:
    x: int

C(x=1) # ok

C(x=1.0) # TypeCheckError: C.x = float(1.0) is not int
```

### Super friendly stack trace

This is the output of test cases. You can run the test yourself!

```
================================== 01-simple ===================================                                                                     

[ PASS ] 1 is int => True
[REASON] Type check passed

[ PASS ] 1.0 is int => False                                                                                                                         
[REASON] float(1.0) is not int                                                                                                                       

[ PASS ] [1, 2, 3] is list[int] => True                                                                                                              
[REASON] Type check passed

[ PASS ] [1, 2, 3.0] is list[int] => False                                                                                                           
[REASON] list[2] = float(3.0) is not int                                                                                                             

[ PASS ] 1 is Literal[1] => True                                                                                                                     
[REASON] Type check passed

[ PASS ] 2 is Literal[1] => False                                                                                                                    
[REASON] int(2) is not Literal[1]                                                                                                                    

[ PASS ] 'alex' is Literal['alex', 'bob'] => True                                                                                                    
[REASON] Type check passed

[ PASS ] 'alex' is Literal['bob'] => False                                                                                                           
[REASON] str('alex') is not Literal['bob']                                                                                                           

================================= 02-multiple ==================================                                                                     

[ PASS ] [1, '2', 3.0] is list[int, str, float] => True                                                                                              
[REASON] Type check passed

[ PASS ] [1, '2', '3'] is list[int, str, float] => False                                                                                             
[REASON] list[2] = str('3') is not float                                                                                                             

[ PASS ] [1, '2'] is list[int, str, float] => False                                                                                                  
[REASON] list([1, '2']) is not list[int, str, float]                                                                                                 

[ PASS ] (1, '2', 3.0) is tuple[int, str, float] => True                                                                                             
[REASON] Type check passed

[ PASS ] (1, '2', '3') is tuple[int, str, float] => False                                                                                            
[REASON] tuple[2] = str('3') is not float                                                                                                            

[ PASS ] {1, 3.0, '2'} is set[int | str | float] => True                                                                                             
[REASON] Type check passed

[ PASS ] {None, 1, '2'} is set[int | str | float] => False                                                                                           
[REASON] set['?'] = NoneType(None) is not int | str | float                                                                                          

[ PASS ] {1: '2', 3: 4.0} is dict[int, str | float] => True                                                                                          
[REASON] Type check passed

[ PASS ] {1: '2', '3': 4.0} is dict[int, str | float] => False                                                                                       
[REASON] dict<key> = str('3') is not int                                                                                                             

[ PASS ] {1: '2', 3: None} is dict[int, str | float] => False                                                                                        
[REASON] dict[3] = NoneType(None) is not str | float                                                                                                 

================================== 03-nested ===================================                                                                     

[ PASS ] [[1, 2], [3, 4]] is list[list[int]] => True                                                                                                 
[REASON] Type check passed

[ PASS ] [[1, 2], [3, '4']] is list[list[int]] => False                                                                                              
[REASON] list[1][1] = str('4') is not int                                                                                                            

================================== 04-unions ===================================                                                                     

[ PASS ] [[1, 2], [3.0, 4.0]] is list[list[int] | list[float]] => True                                                                               
[REASON] Type check passed

[ PASS ] [[1, 2.0], [3, 4.0]] is list[list[int] | list[float]] => False                                                                              
[REASON] list[0] = list([1, 2.0]) is not list[int] | list[float]                                                                                     

================================== 05-inherit ==================================                                                                     

[ PASS ] [1, 2, 3] is A => True                                                                                                                      
[REASON] Type check passed

[ PASS ] [1, 2, 0.0] is A => False                                                                                                                   
[REASON] A[2] = float(0.0) is not int                                                                                                                

[ PASS ] B(x=1, y='2') is tests.05-inherit.B[int, str] => True                                                                                       
[REASON] Type check passed

[ PASS ] B(x=1, y=2.0) is tests.05-inherit.B[int, str] => False                                                                                      
[REASON] B.y = float(2.0) is not str                                                                                                                 

=================================== 06-guard ===================================                                                                     

[ PASS ] C([1, 2, 3]) is C => True                                                                                                                   
[REASON] Type check passed

[ PASS ] C([1, 2, 0.0]) is C => False                                                                                                                
[REASON] C[2] = float(0.0) is not int                                                                                                                

[ PASS ] C(x=1, y=2.0) is C => True                                                                                                                  
[REASON] Type check passed

[ PASS ] C(x=1.0, y=2) is C => False                                                                                                                 
[REASON] C.x = float(1.0) is not int                                                                                                                 

[ PASS ] add(1, 2) is int => True                                                                                                                    
[REASON] Type check passed

[ PASS ] add('1', '2') is str => True                                                                                                                
[REASON] Type check passed

[ PASS ] add([1], [2]) is int | str => False                                                                                                         
[REASON] list([1, 2]) is not int | str                                                                                                               

[ PASS ] All 33 tests passed
```
