# **scalc** - sets calculator

-----

##### All example assumes that files *a.txt*, *b.txt* and *c.txt* are located in the project root directory with content described
```sh
> cat a.txt
> 1
> 2
> 3
>
> cat b.txt
> 2
> 3
> 4
>
> cat c.txt
> 3
> 4
> 5
```

-----

### Implemented functions:
  - **SUM** - evaluate disjunction of sets:
 ```sh
 > make run s="[SUM a.txt b.txt]"
 > 1
 > 2
 > 3
 > 4
 ```

- **INT** - evaluate conjunction of sets:
 ```sh
 > make run s="[INT b.txt c.txt]"
 > 3
 > 4
 ```

- **DIF** - evaluate diff:
 ```sh
 > make run s="[DIF a.txt c.txt]"
 > 1
 > 2
 ```

### Functions can be nested:

```sh
> make run s="[ SUM [ DIF a.txt b.txt c.txt ] [ INT b.txt c.txt ] ]"
> 1
> 3
> 4
```

-----

## Limitations:

- File names should match regex: `^[a-z][a-z0-9_\./]*$`
- In case if you would to implement new functions, all functions names should match regex: `^[A-Z][A-Z_]*$`

-----

## Tests:
To run tests you just have to execute command: `make test`. Tests will be runned in docker container.

-----

## Run in docker:
To run scalc in docker container you just have to execute `make run s="{source string}"`.
Note, if you run **scalc** in docker, all files used in `{source string}` should be located inside project root directory. The directory will be mounted to container as volume.

-----

## Run on host OS:
To run on **scalc** on host OS you must have installed python 3.7 or greater.
Then just run command: `python -m scalc "{source string}"`

-----

## Implementation notes:

##### **scalc** consists of three main parts:
- **tokens** - module which is responsible for parsing source string and generating syntax tokens.
- **compiler** - module which is responsible for compiling parsed tokens into executable expressions.
- **executor** - module which is responsible for executing compiled expressions.
