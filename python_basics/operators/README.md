# Python operators



## Comparison operators

| Operator | Name                     | Example |
| :------- | :----------------------- | :------ |
| ==       | Equal                    | x == y  |
| !=       | Not equal                | x != y  |
| >        | Greater than             | x > y   |
| <        | Less than                | x < y   |
| >=       | Greater than or equal to | x >= y  |
| <=       | Less than or equal to    | x <= y  |



## Logical operators:



| Operator | Description                                             | Example              |
| :------- | :------------------------------------------------------ | :------------------- |
| and      | Returns True if both statements are true                | x < 2 and x < 20     |
| or       | Returns True if one of the statements is true           | x < 2 or x < 5       |
| not      | Reverse the result, returns False if the result is true | not(x < 2 and x < 5) |



## Identity operators

Identity operators are used to compare the objects, not if they are equal, but if they are actually the same object, with the same memory location:

| Operator | Description                                            | Example    |
| :------- | :----------------------------------------------------- | :--------- |
| is       | Returns True if both variables are the same object     | x is y     |
| is not   | Returns True if both variables are not the same object | x is not y |



## Membership operators

Membership operators are used to test if a sequence is presented in an object:

| Operator | Description                                                  | Example    |
| :------- | :----------------------------------------------------------- | :--------- |
| in       | Returns True if a sequence with the specified value is present in the object | x in y     |
| not in   | Returns True if a sequence with the specified value is not present in the object | x not in y |



## Bitwise operators

Bitwise operators are used to compare binary numbers

| Operator | Name                 | Description                                                  | Example |
| :------- | :------------------- | :----------------------------------------------------------- | ------- |
| &        | AND                  | Sets each bit to 1 if both bits are 1                        | x & y   |
| \|       | OR                   | Sets each bit to 1 if one of two bits is 1                   | x \| y  |
| ^        | XOR                  | Sets each bit to 1 if only one of two bits is 1              | x ^ y   |
| ~        | NOT                  | Inverts all the bits                                         | ~x      |
| <<       | Zero fill left shift | Shift left by pushing zeros in from the right and let the leftmost bits fall off | x<<     |
| >>       | Signed right shift   | Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off. | x>>     |



```python
a = 10  # 1010   2**3 + 2**1  
b = 4   # 0010   2**2
print(f"a = {a:2} in binary is {bin(a)[2:]}")
print(f"b = {b:2} in binary is {bin(b)[2:]}")
print(f"bitwise AND operation:         a & b = {a & b}")
print(f"bitwise OR operation:          a | b = {a | b}") 
print(f"bitwise NOT operation:            ~a = {~a}")
print(f"bitwise XOR operation:          a^b  = {a ^ b}")
print(f'bitwise zero fill left shift   a<<0  = {a <<0}')
print(f'bitwise zero fill left shift   a<<1  = {a <<1}')
print(f'bitwise zero fill left shift   a<<2  = {a <<2}')
print(f'bitwise right shift            a>>0  = {a >>0}')
print(f'bitwise right shift            a>>1  = {a >>1}')
print(f'bitwise right shift            a>>2  = {a >>2}')
```

```
a = 10 in binary is 1010
b =  4 in binary is 100
bitwise AND operation:         a & b = 0
bitwise OR operation:          a | b = 14
bitwise NOT operation:            ~a = -11
bitwise XOR operation:          a^b  = 14
bitwise zero fill left shift   a<<0  = 10
bitwise zero fill left shift   a<<1  = 20
bitwise zero fill left shift   a<<2  = 40
bitwise right shift            a>>0  = 10
bitwise right shift            a>>1  = 5
bitwise right shift            a>>2  = 2
```

Note that

- `x>>1` is the same as `x//2`
- `x = 14` then `bin(x)` is `'1110'`
- `x = 7`    then `bin(x)` is `'111'`
- 14//2 is 7 which is equivalent to `'1110'` right shift which becomes `'0111'`
- 14//2 is 7 and 7//2 is 3 therefore  (14>>1)>>1 is 3
- In this case 3 is in binary 11 which is the same as 1110 with two right bit shifts,



```python
def right_bit_shift(x,n):
     return x>>n

def right_bit_shift_conversion(x,n):
    return x//(2**n)
 
def left_bit_shift(x,n):
     return x<<n

def left_bit_shift_conversion(x,n):
    return x*2**n

print(f'left_bit_shift(7,2)={left_bit_shift(7,2)}')
print(f'left_bit_shift_conversion(7,2)={left_bit_shift_conversion(7,2)}')

print(f'right_bit_shift(14,2)={right_bit_shift(14,2)}')
print(f'right_bit_shift_conversion(14,2)={right_bit_shift_conversion(14,2)}')
```

```
left_bit_shift(7,2)=28
left_bit_shift_conversion(7,2)=28
right_bit_shift(14,2)=3
right_bit_shift_conversion(14,2)=3
```



## Set operators

| Operator | Name                 | Description                           |
| :------- | :------------------- | :------------------------------------ |
| &        | Intersection         | Intersecttion betwwen two sets        |
| \|       | Union                | Union between two sets                |
| ^        | Diference            | Diference between two sets            |
| ^        | Symmetric Difference | Symmetric difference between two sets |



```python
A = set([0, 2, 4, 6, 8])
B = set([1, 2, 3, 4, 5])

print(f"A={A}")
print(f"B={B}")
print("A Union B         ---> A | B =", A | B)
print("A Intersection B  ---> A & B =", A & B)
print("A Difference B    ---> A - B =", A - B)  
print("A Sym-difference B --> A ^ B =", A ^ B)
```

```
A={0, 2, 4, 6, 8}
B={1, 2, 3, 4, 5}
A Union B         ---> A | B = {0, 1, 2, 3, 4, 5, 6, 8}
A Intersection B  ---> A & B = {2, 4}
A Difference B    ---> A - B = {0, 8, 6}
A Sym-difference B --> A ^ B = {0, 1, 3, 5, 6, 8}
```

