# Extensive Language for Data Analysis (ELDA)

## Abput ELDA
### Vision / Purpose
Extensive Language for Data Analysis is born with the vision of providing a tool for data analysis that results from a commitment in equal parts between the learning of a programming language focused on data analysis, and the efficient handling of data for processing in useful calculations for anyone with context in data science. All this with the purpose that the language serves as a facilitator for users without technological context in the adoption of analysis tools, thus being a bridge between people with mathematical knowledge but without programming knowledge to the use of more robust data analysis and manipulation tools.

As a result of this, two main conclusions can be drawn. First, it is not expected that language users have prior knowledge about programming of any kind, since it is expected that this knowledge can be obtained through the use of it. And second, once the basic knowledge about the programming oriented to the data analysis is achieved, calculations can be made with enough depth for the language to be considered useful in the prototyping of more robust solutions.

### Main objective
The objective of E.L.D.A is to be a facilitator for people with no programming experience who wish to do basic statistical calculations such as: mean, variance, standard deviation, clustering, data classification, graph plotting, etc. It aims to shorten the gap between people with and without experience in technology such as graduates and students.
 
ELDA belongs to the same category of languages as R, MATLAB and Octave, which allow matrix manipulation and data mapping. The difference between these languages that are more established and our project is that ELDA does not intend to do everything that these languages do; Analysis of time series, for example, are things that are beyond the scope of this compiler. The main purpose of our compiler is to be the first step in the transition to use these languages.

## Quick Reference Manual

### Installation
Since ELDA is a language completely developed over python, it is distributed as a pyhton package and hence available
through the package manager PIP.

To install ELDA, simply run:
```
pip install elda
```

This will install all required packages and make the language compiler and virtual machine available through a command
line interface. This command has 2 parts: The compilation and the execution, to compile a program run:
```bash
elda -c <file>
```

This will generate an object file with the `.eo` extension and the same name as your program. To execute it, simply run:
```bash
elda -e <compiled_file>
```
*NOTE*: Depending on your existing python setup, the first time that elda is called may take some time to execute.
This is due to matplotlib (which is used under the hood) caching some files needed to execute and will only happen
once.

### Language Examples
An ELDA program is heavily structured, with declarations, statements and returns all following a set order. For example,
to create a recursive fibonacci program, the return value should be stored and return should be called only once at the 
end of the function, like so:
```
int fibonacci(int x) {
    int return_value;
    if (x == 0) {
        return_value = 0;
    }
    if (x == 1) {
        return_value = 1;
    }
    if (x != 0 and x != 1) {
        return_value = fibonacci(x-1) + fibonacci(x-2);
    }
    return return_value;
}

void main() {
    out(fibonacci(10));
}
```
### Array handling
To declare arrays with ELDA, you must add the size of the array *after* the type declaration but *before* the variable id.
For example, a simple program that handles matrixes:
```
int[5] vectorA = [1,2,3,4,5];
int[5] vectorB = [5,4,3,2,1];

int[5][5] matrixA = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]];
int[5][5] matrixB = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]];

int[5][5] mult;
int[5][5] trans;
int[5] sum;

void print_matrix(int w) {
    string row = "";
    for i with range(0, 5) {
        for j with range(0, 5) {
            if (w == 1) {
                row = row + mult[i][j] + " ";
            } else {
                row = row + trans[i][j] + " ";
            }
        }
        out(row);
        row = "";
    }
}

void print_vector() {
    string row = "";
    for i with range(0, 5) {
        row = row + sum[i] + " ";
    }
    out(row);
    row = "";
}

void multiply_matrixes() {
    for i with range(0, 5) {
        for j with range(0, 5) {
            for k with range(0, 5) {
                mult[i][j] = mult[i][j] + matrixA[i][k] * matrixB[k][j];
            }
        }
    }
    print_matrix(1);
}

void sum_vectors() {
    for i with range(0, 5) {
        sum[i] = vectorA[i] + vectorB[i];
    }
    print_vector();
}

void transpose_matrix() {
    for i with range(0, 5) {
        for j with range(0, 5) {
            trans[j][i] = matrixA[i][j];
        }
    }
    print_matrix(2);
}

void main() {
    out("Matrix multiplication of 5x5");
    multiply_matrixes();

    out("Vector sum");
    sum_vectors();

    out("Transposed matrix of matrixA");
    transpose_matrix();
}
```
Lastly, ELDA comes with some analysis functions out of the box. This functions can be used by simply calling them
from anywhere inside the program, and since they are part of the language, no module or import is required.
```
int[50] x = [4, 5, 7, 8, 11, 14, 16, 18, 19, 20, 25, 27, 28, 33, 34, 35, 37, 38, 41, 43, 44, 45, 48, 49, 50, 52, 53, 55, 56, 58, 63, 64, 66, 67, 71, 73, 74, 76, 79, 81, 83, 84, 85, 86, 87, 90, 92, 94, 96, 100];
int[50] y = [2, 4, 5, 6, 10, 11, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 34, 35, 37, 40, 41, 45, 46, 50, 51, 52, 54, 57, 59, 60, 61, 64, 65, 66, 69, 70, 78, 82, 83, 85, 86, 91, 92, 95, 97, 98, 99];

int[50] reg_x;
int[50] reg_y;

int[50][2] xy;

void display_data(int v) {
	if (v == 1) {
		out("Data for x");
		out("Min of x: " + min(x));
		out("Max of x: " + max(x));
		out("Mean of x: " + mean(x));
		out("Median of x: " + median(x));
		out("Std deviation of x: " + std(x));
		out("Variance of x: " + var(x));
	} else {
		out("Data for y");
		out("Min of y: " + min(y));
		out("Max of y: " + max(y));
		out("Mean of y: " + mean(y));
		out("Median of y: " + median(y));
		out("Std deviation of y: " + std(y));
		out("Variance of y: " + var(y));
	}
}

void compute_linear_regression() {
	float[2] reg_params = linear_regression(x, y);
	int val_x = 2;
	string res = "Linear function: " + reg_params[0];
	res = res + "x + " + reg_params[1];

	out(res);
	for i with range(0, 50) {
		reg_x[i] = val_x;
		reg_y[i] = reg_params[0] * val_x + reg_params[1];
		val_x = val_x + 2;
	}
	graph(reg_x, reg_y, "plot");
}

void compute_logistic_regression() {
	float[2] reg_params = logistic_regression(x, y);
	
	out("Logistic Regression parameters: ");
	out(reg_params[0]);
	out(reg_params[1]);
}

void populate_xy() {
	for i with range(0, size(x)) {
		xy[i][0] = x[i];
		xy[i][1] = y[i];
	}
}

void compute_kmeans() {
	float[2][2] centers = k_means(2, xy);
	float[2] val_x;
	float[2] val_y;

	val_x[0] = centers[0][0];
	val_y[0] = centers[0][1];
	val_x[1] = centers[1][0];
	val_y[1] = centers[1][1];

	out("First center at: ");
	out("X: " + val_x[0]);
	out("Y: " + val_y[0]);

	out("Second center at: ");
	out("X: " + val_x[1]);
	out("Y: " + val_y[1]);

	graph(val_x, val_y, "scatter");
}

void main() {
	display_data(1);
	out("----------------------");
	display_data(2);

	graph(x, y, "scatter");

	compute_linear_regression();
	compute_logistic_regression();

	populate_xy();
	compute_kmeans();
}
```
### Available Special Functions

- mean(arr) - Compute the mean of an array of data
    - arr: a one dimensional array.
    - returns: a float with the mean of the array. 
    
- min(arr) - Get the minimum value on an array
    - arr: a one dimensional array.
    - returns: a float with the minimum value of the array.

- max(arr) - Get the maximum value on an array
    - arr: a one dimensional array.
    - returns: a float with the maximum value of the array.
    
- median(arr) - Get the median value on an array
    - arr: a one dimensional array.
    - returns: a float with the median value of the array.
    
- var(arr) - Get the variance value on an array
    - arr: a one dimensional array.
    - returns: a float with the variance value of the array.

- std(arr) - Get the standard deviation value on an array
    - arr: a one dimensional array.
    - returns: a float with the standard deviation value of the array.
    
- linear_regression(arr_x, arr_y) - Get the linear regression parameters given two arrays representing x values and y
values.
    - arr_x: a one dimensional array.
    - arr_y: a one dimensional array.
    - returns: an array with the regression parameters.

- logistic_regression(arr_x, arr_y) - Get the logistic regression parameters given two arrays representing x values and y
values.
    - arr_x: a one dimensional array.
    - arr_y: a one dimensional array.
    - returns: an array with the regression parameters.

- k_means(k, arr_xy) - Get the k cluster centers given one array representing x and y value pairs.
    - k: an int representing the number of clusters.
    - arr_xy: a two dimensional array represnting x and y value pairs. Ex: [[1, 2], [2, 3], [4, 5]].
    - returns: an array with the cluster centers c and y coordinates.
    
- size(arr) - Get the size of an array
    - arr: a one dimensional or two dimensional array.
    - returns: an int with the size of the array.
    
- type(var) - Get the type of the variable as a string
    - arr: a variable, cannot be an array.
    - returns: a string with the type name.