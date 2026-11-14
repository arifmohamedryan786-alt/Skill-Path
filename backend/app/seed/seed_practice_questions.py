"""
SkillPath Comprehensive Practice Question Bank
50 Curated Programming & Problem-Solving Questions across 5 Core Categories:
1. C Programming (10)
2. Python (10)
3. Java (10)
4. Data Structures (10)
5. DSA (10)
"""

PRACTICE_QUESTIONS_DATA = [
    # =========================================================================
    # 1. C PROGRAMMING (10 Questions)
    # =========================================================================
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Reverse a Positive Integer",
        "difficulty": "Beginner",
        "order_index": 1,
        "description": "Write a C function to reverse the digits of a given positive integer `n`. For instance, if the input is 12345, your function should return 54321.",
        "example_input": "n = 12345",
        "example_output": "54321",
        "hint": "Use a while loop with modulo (%) to extract the last digit (`n % 10`) and integer division (`n / 10`) to discard it. Accumulate the result with `rev = rev * 10 + rem`.",
        "starter_code": """#include <stdio.h>

long long reverseNumber(long long n) {
    // Write your solution here
    return 0;
}

int main() {
    long long n = 12345;
    printf("Reversed: %lld\\n", reverseNumber(n));
    return 0;
}
""",
        "solution": """#include <stdio.h>

long long reverseNumber(long long n) {
    long long reversed = 0;
    while (n > 0) {
        int remainder = n % 10;
        reversed = reversed * 10 + remainder;
        n /= 10;
    }
    return reversed;
}

int main() {
    long long n = 12345;
    printf("Reversed: %lld\\n", reverseNumber(n));
    return 0;
}
""",
        "approach": "1. Initialize `reversed` to 0.\n2. In a loop while `n > 0`, extract the units digit with `remainder = n % 10`.\n3. Shift `reversed` left by multiplying by 10 and add the remainder.\n4. Truncate `n` by dividing by 10.\n5. Return `reversed`.",
        "explanation": "Modulo by 10 isolates the least-significant digit. Multiplying the accumulator by 10 shifts existing digits one place to the left, correctly assembling the reversed number from left to right.",
        "time_complexity": "O(log10(N))",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Check Whether a Number is Prime",
        "difficulty": "Beginner",
        "order_index": 2,
        "description": "Given an integer `n`, write a C program to determine whether it is a prime number. A prime number is a natural number greater than 1 that cannot be formed by multiplying two smaller natural numbers.",
        "example_input": "n = 29",
        "example_output": "1 (True)",
        "hint": "Any factor of `n` must occur on or before `sqrt(n)`. If no number from 2 up to `sqrt(n)` divides `n` evenly, then `n` is prime.",
        "starter_code": """#include <stdio.h>
#include <stdbool.h>

bool isPrime(int n) {
    // Write your code here
    return false;
}
""",
        "solution": """#include <stdio.h>
#include <stdbool.h>

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    }
    return true;
}
""",
        "approach": "1. Guard against numbers <= 1.\n2. Handle 2 and 3 as initial primes.\n3. Eliminate even numbers and multiples of 3.\n4. Check divisibility up to `sqrt(n)` using step increments of 6 (checking `i` and `i + 2`).",
        "explanation": "All primes greater than 3 can be expressed in the form 6k ± 1. Checking up to the square root reduces unnecessary iterations from O(N) to O(sqrt(N)).",
        "time_complexity": "O(sqrt(N))",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Find the Largest Element in an Array",
        "difficulty": "Beginner",
        "order_index": 3,
        "description": "Given an array of `n` integers, find and return the largest element present in the array.",
        "example_input": "arr[] = {14, 82, 35, 99, 41}, n = 5",
        "example_output": "99",
        "hint": "Initialize `max` with the first element `arr[0]`, then traverse the array comparing each element.",
        "starter_code": """#include <stdio.h>

int findMax(int arr[], int n) {
    // Return largest integer
    return 0;
}
""",
        "solution": """#include <stdio.h>

int findMax(int arr[], int n) {
    if (n <= 0) return -1;
    int maxVal = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > maxVal) {
            maxVal = arr[i];
        }
    }
    return maxVal;
}
""",
        "approach": "1. Set `maxVal = arr[0]`.\n2. Iterate through indices 1 to n-1.\n3. If `arr[i] > maxVal`, update `maxVal = arr[i]`.\n4. Return `maxVal`.",
        "explanation": "A single linear pass inspects every element once to guarantee finding the true maximum.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Palindrome Number Check",
        "difficulty": "Beginner",
        "order_index": 4,
        "description": "Determine whether an integer `x` is a palindrome. An integer is a palindrome when it reads the same backwards as forwards (e.g. 121 is a palindrome, but -121 and 10 are not).",
        "example_input": "x = 121",
        "example_output": "1 (True)",
        "hint": "Negative numbers are never palindromes due to the leading minus sign. Reverse the number and compare with the original value.",
        "starter_code": """#include <stdio.h>
#include <stdbool.h>

bool isPalindrome(int x) {
    // Write your code here
    return false;
}
""",
        "solution": """#include <stdio.h>
#include <stdbool.h>

bool isPalindrome(int x) {
    if (x < 0) return false;
    long long original = x;
    long long reversed = 0;
    while (x > 0) {
        reversed = reversed * 10 + (x % 10);
        x /= 10;
    }
    return original == reversed;
}
""",
        "approach": "1. Return false if x < 0.\n2. Store copy of original number.\n3. Reverse digits using `% 10` and `/ 10`.\n4. Return comparison `original == reversed`.",
        "explanation": "Reversing the number and testing equality with the preserved original confirms whether symmetry holds.",
        "time_complexity": "O(log10(N))",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Fibonacci Series Up to N Terms",
        "difficulty": "Beginner",
        "order_index": 5,
        "description": "Write a C program to compute the first `n` terms of the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, ...).",
        "example_input": "n = 6",
        "example_output": "0 1 1 2 3 5",
        "hint": "Maintain two tracking variables: `first = 0` and `second = 1`. In each iteration compute `next = first + second` and advance the pointers.",
        "starter_code": """#include <stdio.h>

void printFibonacci(int n) {
    // Print first n Fibonacci numbers
}
""",
        "solution": """#include <stdio.h>

void printFibonacci(int n) {
    if (n <= 0) return;
    long long first = 0, second = 1;
    for (int i = 0; i < n; i++) {
        printf("%lld ", first);
        long long next = first + second;
        first = second;
        second = next;
    }
    printf("\\n");
}
""",
        "approach": "1. Check edge case `n <= 0`.\n2. Print `first`.\n3. Calculate `next = first + second`.\n4. Shift `first = second` and `second = next`.\n5. Repeat `n` times.",
        "explanation": "Iterative Fibonacci avoids the exponential O(2^N) overhead of naive recursion by keeping only the last two computed terms.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Swap Two Numbers Using Pointers",
        "difficulty": "Intermediate",
        "order_index": 6,
        "description": "Implement a C function `void swap(int *a, int *b)` that swaps the values of two integer variables using memory pointers (pass-by-reference).",
        "example_input": "a = 10, b = 20",
        "example_output": "a = 20, b = 10",
        "hint": "Dereference the pointers using the `*` operator to access and exchange the actual stored values in memory.",
        "starter_code": """#include <stdio.h>

void swap(int *a, int *b) {
    // Swap values through dereferenced pointers
}
""",
        "solution": """#include <stdio.h>

void swap(int *a, int *b) {
    if (a == NULL || b == NULL) return;
    int temp = *a;
    *a = *b;
    *b = temp;
}
""",
        "approach": "1. Verify pointers are not NULL.\n2. Store value pointed to by `a` into temporary variable `temp`.\n3. Assign value pointed to by `b` into memory at `*a`.\n4. Assign `temp` into memory at `*b`.",
        "explanation": "In C, function arguments are passed by value. Passing addresses via pointers allows the function to directly modify variables in the caller's stack frame.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Count Vowels and Consonants in a String",
        "difficulty": "Intermediate",
        "order_index": 7,
        "description": "Given a null-terminated string `str`, count the total number of vowels and consonants. Ignore digits, spaces, and punctuation.",
        "example_input": "str = \"SkillPath 2026\"",
        "example_output": "Vowels: 2, Consonants: 7",
        "hint": "Convert characters to lowercase or check both cases using `tolower()` from `<ctype.h>` and `isalpha()` to check for alphabetic letters.",
        "starter_code": """#include <stdio.h>
#include <ctype.h>

void countVowelsConsonants(const char *str, int *vowels, int *consonants) {
    // Write your code here
}
""",
        "solution": """#include <stdio.h>
#include <ctype.h>

void countVowelsConsonants(const char *str, int *vowels, int *consonants) {
    *vowels = 0;
    *consonants = 0;
    while (*str) {
        char c = tolower(*str);
        if (c >= 'a' && c <= 'z') {
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                (*vowels)++;
            } else {
                (*consonants)++;
            }
        }
        str++;
    }
}
""",
        "approach": "1. Reset counts to 0.\n2. Traverse characters using pointer increment until `\\0`.\n3. Check if character is alphabetic.\n4. Increment vowel count if matched with 'a', 'e', 'i', 'o', 'u', otherwise consonant count.",
        "explanation": "Traversing through pointer dereferencing `*str` until the null terminator allows linear O(N) evaluation with zero memory allocations.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Dynamic Array Allocation with malloc and free",
        "difficulty": "Intermediate",
        "order_index": 8,
        "description": "Write a C function that dynamically allocates an integer array of size `n` using `malloc`, populates it with square numbers `(i * i)`, calculates the sum, and properly frees the memory to prevent leaks.",
        "example_input": "n = 5",
        "example_output": "Sum: 30 (0 + 1 + 4 + 9 + 16)",
        "hint": "Check if `malloc` returns `NULL`. Always pair every `malloc` with `free()` when dynamic heap memory is no longer required.",
        "starter_code": """#include <stdio.h>
#include <stdlib.h>

long long sumOfSquares(int n) {
    // Allocate dynamically, sum, and free
    return 0;
}
""",
        "solution": """#include <stdio.h>
#include <stdlib.h>

long long sumOfSquares(int n) {
    if (n <= 0) return 0;
    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) {
        return -1; // Allocation failure
    }

    long long sum = 0;
    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
        sum += arr[i];
    }

    free(arr);
    arr = NULL;
    return sum;
}
""",
        "approach": "1. Allocate heap memory: `malloc(n * sizeof(int))`.\n2. Guard against allocation failure.\n3. Compute values and accumulate sum.\n4. Free memory with `free(arr)` and set pointer to NULL.",
        "explanation": "Dynamic memory management is central to C. Allocating on the heap avoids stack overflow for large datasets, but requires strict deallocation to prevent memory leaks.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "In-Place String Reversal Using Pointers",
        "difficulty": "Advanced",
        "order_index": 9,
        "description": "Reverse a mutable C string in-place without allocating an auxiliary string buffer. The function should mutate the original character array.",
        "example_input": "str = \"datastructures\"",
        "example_output": "\"serutcurtsatad\"",
        "hint": "Set one pointer at the start and another at the end of the string (before `\\0`). Swap characters and move pointers inward until they meet.",
        "starter_code": """#include <stdio.h>
#include <string.h>

void reverseStringInPlace(char *str) {
    // In-place pointer swap
}
""",
        "solution": """#include <stdio.h>
#include <string.h>

void reverseStringInPlace(char *str) {
    if (str == NULL || *str == '\\0') return;
    char *start = str;
    char *end = str + strlen(str) - 1;

    while (start < end) {
        char temp = *start;
        *start = *end;
        *end = temp;
        start++;
        end--;
    }
}
""",
        "approach": "1. Point `start` to head of string.\n2. Point `end` to `str + len - 1`.\n3. Swap `*start` and `*end`.\n4. Increment `start`, decrement `end`.\n5. Terminate when pointers cross.",
        "explanation": "The two-pointer technique achieves in-place reversal in O(N/2) swaps with strict O(1) auxiliary space.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "C Programming",
        "category_slug": "c-programming",
        "title": "Implement Custom my_strlen and my_strcpy",
        "difficulty": "Advanced",
        "order_index": 10,
        "description": "Implement your own versions of the standard C library functions `strlen` and `strcpy` using pointer arithmetic without including `<string.h>`.",
        "example_input": "src = \"SkillPath\"",
        "example_output": "len = 9, copied = \"SkillPath\"",
        "hint": "For length, increment pointer until `*ptr == '\\0'`. For copy, assign `*dest = *src` in a loop until null terminator is copied.",
        "starter_code": """#include <stdio.h>

size_t my_strlen(const char *str) {
    // Write your code here
    return 0;
}

char *my_strcpy(char *dest, const char *src) {
    // Write your code here
    return dest;
}
""",
        "solution": """#include <stdio.h>

size_t my_strlen(const char *str) {
    const char *ptr = str;
    while (*ptr != '\\0') {
        ptr++;
    }
    return (size_t)(ptr - str);
}

char *my_strcpy(char *dest, const char *src) {
    char *d = dest;
    while ((*d++ = *src++) != '\\0') {
        // Copy until null byte
    }
    return dest;
}
""",
        "approach": "1. In `my_strlen`, advance `ptr` to null byte; the difference `ptr - str` equals length.\n2. In `my_strcpy`, assign each character from source to destination including the closing `\\0`.\n3. Return destination pointer.",
        "explanation": "Demonstrates low-level pointer arithmetic and idiomatic C copy idiom `while((*d++ = *src++))`, fundamental to systems programming.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },

    # =========================================================================
    # 2. PYTHON (10 Questions)
    # =========================================================================
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Reverse a String",
        "difficulty": "Beginner",
        "order_index": 11,
        "description": "Write a Python function `reverse_string(s: str) -> str` that returns the reversed version of a given input string.",
        "example_input": "s = \"skillpath\"",
        "example_output": "\"htaplliks\"",
        "hint": "Python strings support extended slice syntax `s[start:stop:step]`. A negative step reverses the sequence.",
        "starter_code": """def reverse_string(s: str) -> str:
    # Write your solution here
    pass
""",
        "solution": """def reverse_string(s: str) -> str:
    return s[::-1]
""",
        "approach": "1. Use Python's built-in sequence slicing `s[::-1]`.\n2. Slicing with a step of `-1` starts at the end and steps backward to the beginning.",
        "explanation": "Python string slicing is implemented in C under the hood, making `s[::-1]` both the most idiomatic and fastest way to reverse strings in Python.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Count Character Frequencies in a String",
        "difficulty": "Beginner",
        "order_index": 12,
        "description": "Given a string `s`, count the frequency of each character and return the result as a dictionary.",
        "example_input": "s = \"engineering\"",
        "example_output": "{'e': 3, 'n': 3, 'g': 2, 'i': 2, 'r': 1}",
        "hint": "Iterate through characters using a standard dictionary with `.get(char, 0) + 1` or Python's `collections.Counter`.",
        "starter_code": """def char_frequency(s: str) -> dict[str, int]:
    # Write your solution here
    pass
""",
        "solution": """def char_frequency(s: str) -> dict[str, int]:
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq
""",
        "approach": "1. Create an empty dictionary `freq`.\n2. Iterate through each character in the string.\n3. Increment count using `dict.get(char, 0) + 1`.\n4. Return the resulting dictionary.",
        "explanation": "Dictionary key lookups in Python operate in amortized O(1) time via hash tables. A single pass over N characters yields O(N) overall runtime.",
        "time_complexity": "O(N)",
        "space_complexity": "O(K) where K is number of unique characters"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Find All Duplicate Elements in a List",
        "difficulty": "Beginner",
        "order_index": 13,
        "description": "Given a list of numbers or items, return a list containing all elements that appear more than once.",
        "example_input": "nums = [1, 3, 4, 2, 2, 3, 5]",
        "example_output": "[3, 2]",
        "hint": "Use a `seen` set to track items observed so far, and a `duplicates` set to record duplicates without repeats.",
        "starter_code": """def find_duplicates(items: list) -> list:
    # Write your solution here
    pass
""",
        "solution": """def find_duplicates(items: list) -> list:
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
""",
        "approach": "1. Initialize two sets: `seen` and `duplicates`.\n2. For each element in list, check if present in `seen`.\n3. If present, add to `duplicates`.\n4. Otherwise, add to `seen`.\n5. Convert `duplicates` set to list and return.",
        "explanation": "Set membership checking is O(1) on average. Using sets ensures we collect duplicates efficiently without duplicate listings.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Check if Two Strings are Anagrams",
        "difficulty": "Beginner",
        "order_index": 14,
        "description": "Write a function `is_anagram(s1: str, s2: str) -> bool` to determine if two given strings are anagrams of each other (contain identical letters in any order).",
        "example_input": "s1 = \"listen\", s2 = \"silent\"",
        "example_output": "True",
        "hint": "Two strings are anagrams if their character frequency distributions or sorted characters are identical.",
        "starter_code": """def is_anagram(s1: str, s2: str) -> bool:
    # Write your solution here
    pass
""",
        "solution": """from collections import Counter

def is_anagram(s1: str, s2: str) -> bool:
    clean_s1 = s1.replace(" ", "").lower()
    clean_s2 = s2.replace(" ", "").lower()
    return Counter(clean_s1) == Counter(clean_s2)
""",
        "approach": "1. Strip spaces and normalize to lowercase.\n2. If string lengths differ, immediately return False.\n3. Count frequencies using `Counter` and compare mappings.",
        "explanation": "Counting frequencies using hash tables is O(N) time and handles unicode characters accurately.",
        "time_complexity": "O(N)",
        "space_complexity": "O(K)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "List Comprehension for Filter and Transform",
        "difficulty": "Beginner",
        "order_index": 15,
        "description": "Given a list of integers, write a single list comprehension that squares all even numbers and ignores odd numbers.",
        "example_input": "nums = [1, 2, 3, 4, 5, 6, 7, 8]",
        "example_output": "[4, 16, 36, 64]",
        "hint": "The syntax for filtering in a comprehension is `[expression for item in iterable if condition]`.",
        "starter_code": """def square_evens(nums: list[int]) -> list[int]:
    # Return list comprehension
    pass
""",
        "solution": """def square_evens(nums: list[int]) -> list[int]:
    return [x ** 2 for x in nums if x % 2 == 0]
""",
        "approach": "1. Iterate through elements with `for x in nums`.\n2. Add filter condition `if x % 2 == 0`.\n3. Transform output expression to `x ** 2`.",
        "explanation": "List comprehensions in Python combine map and filter into concise, optimized bytecode executed faster than manual loop appends.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Group Items by Key Function",
        "difficulty": "Intermediate",
        "order_index": 16,
        "description": "Implement a function `group_by(items: list, key_fn) -> dict` that groups elements of a list into a dictionary based on the return value of `key_fn`.",
        "example_input": "words = [\"apple\", \"bat\", \"banana\", \"cup\"], key_fn = len",
        "example_output": "{5: ['apple'], 3: ['bat', 'cup'], 6: ['banana']}",
        "hint": "Use `collections.defaultdict(list)` to append items automatically without manual key initialization.",
        "starter_code": """from collections import defaultdict

def group_by(items: list, key_fn) -> dict:
    # Group items into dictionary
    pass
""",
        "solution": """from collections import defaultdict

def group_by(items: list, key_fn) -> dict:
    grouped = defaultdict(list)
    for item in items:
        key = key_fn(item)
        grouped[key].append(item)
    return dict(grouped)
""",
        "approach": "1. Instantiate `defaultdict(list)`.\n2. For each item, evaluate `key = key_fn(item)`.\n3. Append item to `grouped[key]`.\n4. Convert to standard dict and return.",
        "explanation": "`defaultdict` streamlines the grouping pattern by executing a factory function whenever a key is first accessed, preventing `KeyError`.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Merge Two Dictionaries with Value Resolution",
        "difficulty": "Intermediate",
        "order_index": 17,
        "description": "Given two dictionaries with numeric values, merge them into a single dictionary. If a key appears in both dictionaries, sum their values.",
        "example_input": "d1 = {'a': 10, 'b': 20}, d2 = {'b': 5, 'c': 15}",
        "example_output": "{'a': 10, 'b': 25, 'c': 15}",
        "hint": "Start with a copy of `d1`, then iterate through items of `d2` adding values to existing keys.",
        "starter_code": """def merge_sum_dicts(d1: dict, d2: dict) -> dict:
    # Write your solution here
    pass
""",
        "solution": """def merge_sum_dicts(d1: dict, d2: dict) -> dict:
    merged = dict(d1)
    for k, v in d2.items():
        merged[k] = merged.get(k, 0) + v
    return merged
""",
        "approach": "1. Shallow copy `d1` to `merged`.\n2. Loop through `d2.items()`.\n3. Set `merged[k] = merged.get(k, 0) + v`.\n4. Return `merged`.",
        "explanation": "Iterating through the second dictionary updates overlapping keys in O(1) average lookup time per key.",
        "time_complexity": "O(len(d1) + len(d2))",
        "space_complexity": "O(len(d1) + len(d2))"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Flatten an Arbitrarily Nested List",
        "difficulty": "Intermediate",
        "order_index": 18,
        "description": "Write a recursive function `flatten(nested_list)` that takes a list with arbitrary levels of nested lists and returns a flat 1D list.",
        "example_input": "nested = [1, [2, [3, 4], 5], 6, [7]]",
        "example_output": "[1, 2, 3, 4, 5, 6, 7]",
        "hint": "For each element, check `isinstance(element, list)`. If it is a list, recursively flatten it; otherwise append it to the accumulator.",
        "starter_code": """def flatten(nested_list: list) -> list:
    # Flatten recursively
    pass
""",
        "solution": """def flatten(nested_list: list) -> list:
    flat = []
    for item in nested_list:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat
""",
        "approach": "1. Create an output list `flat`.\n2. Iterate through `nested_list`.\n3. If item is an instance of `list`, recursively call `flatten(item)` and extend.\n4. Otherwise append scalar item.\n5. Return `flat`.",
        "explanation": "Recursive traversal visits every terminal scalar exactly once regardless of nesting depth.",
        "time_complexity": "O(Total elements)",
        "space_complexity": "O(Maximum depth + output size)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Prime Number Generator Using Sieve Algorithm",
        "difficulty": "Advanced",
        "order_index": 19,
        "description": "Implement a Python generator function `generate_primes(limit: int)` that yields prime numbers up to `limit` using the Sieve of Eratosthenes.",
        "example_input": "limit = 20",
        "example_output": "Yields: 2, 3, 5, 7, 11, 13, 17, 19",
        "hint": "Use a boolean array `is_prime = [True] * (limit + 1)`. When a prime `p` is found, mark its multiples `2*p, 3*p...` as False and `yield p`.",
        "starter_code": """from typing import Generator

def generate_primes(limit: int) -> Generator[int, None, None]:
    # Yield primes lazily
    pass
""",
        "solution": """from typing import Generator

def generate_primes(limit: int) -> Generator[int, None, None]:
    if limit < 2:
        return
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for num in range(2, limit + 1):
        if is_prime[num]:
            yield num
            for multiple in range(num * num, limit + 1, num):
                is_prime[multiple] = False
""",
        "approach": "1. Initialize boolean table of size `limit + 1` to True.\n2. Mark 0 and 1 as False.\n3. For each number from 2 to limit, if True, yield the number.\n4. Strike out multiples starting from `num * num` with step `num`.",
        "explanation": "Starting composite marking at `num * num` avoids redundant work. Generators allow memory-friendly streaming of computed primes.",
        "time_complexity": "O(N log(log N))",
        "space_complexity": "O(N)"
    },
    {
        "category": "Python",
        "category_slug": "python",
        "title": "Implement an In-Memory LRU Cache Decorator",
        "difficulty": "Advanced",
        "order_index": 20,
        "description": "Write a custom Python function decorator `@lru_cache(capacity=3)` that caches the results of function calls and evicts the least-recently used entry when capacity is exceeded.",
        "example_input": "calls to expensive_func(1), (2), (3), (4)",
        "example_output": "Evicts key 1 when 4 is called",
        "hint": "Use `collections.OrderedDict`. Moving a key to the end with `move_to_end()` marks it as recently used. `popitem(last=False)` removes the oldest item.",
        "starter_code": """from collections import OrderedDict
from functools import wraps

def lru_cache(capacity: int = 3):
    # Return decorator
    pass
""",
        "solution": """from collections import OrderedDict
from functools import wraps

def lru_cache(capacity: int = 3):
    def decorator(func):
        cache = OrderedDict()
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                cache.move_to_end(key)
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            if len(cache) > capacity:
                cache.popitem(last=False)
            return result
        return wrapper
    return decorator
""",
        "approach": "1. Create closure around `OrderedDict`.\n2. Hash arguments into a cache key tuple.\n3. If cache hit, mark recently used via `move_to_end`.\n4. If cache miss, compute result, insert, and evict head if `len > capacity`.",
        "explanation": "`OrderedDict` maintains double-linked list ordering behind hash table lookups, granting O(1) retrieval and O(1) eviction.",
        "time_complexity": "O(1) per lookup/insertion",
        "space_complexity": "O(Capacity)"
    },

    # =========================================================================
    # 3. JAVA (10 Questions)
    # =========================================================================
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Class and Object Basics (Student Class)",
        "difficulty": "Beginner",
        "order_index": 21,
        "description": "Create a `Student` class in Java with private fields `name`, `rollNumber`, and `grade`. Include a constructor to initialize them and a `displayDetails()` method.",
        "example_input": "Student s = new Student(\"Arif\", 101, \"A\"); s.displayDetails();",
        "example_output": "Name: Arif, Roll: 101, Grade: A",
        "hint": "Declare private fields for encapsulation. Provide a public constructor assigning parameters using the `this` keyword.",
        "starter_code": """public class Student {
    // Declare private fields, constructor, and displayDetails()
}
""",
        "solution": """public class Student {
    private String name;
    private int rollNumber;
    private String grade;

    public Student(String name, int rollNumber, String grade) {
        this.name = name;
        this.rollNumber = rollNumber;
        this.grade = grade;
    }

    public void displayDetails() {
        System.out.println("Name: " + name + ", Roll: " + rollNumber + ", Grade: " + grade);
    }
}
""",
        "approach": "1. Define private member variables for data protection.\n2. Provide parameterized constructor using `this.name = name`.\n3. Implement public display method for formatted output.",
        "explanation": "Encapsulation restricts direct variable access and bundles data with the methods that operate on it, a core tenet of Object-Oriented Programming.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Find Maximum and Minimum in an Array",
        "difficulty": "Beginner",
        "order_index": 22,
        "description": "Write a Java method that accepts an array of integers and finds both the maximum and minimum elements.",
        "example_input": "int[] nums = {5, 2, 9, 1, 7};",
        "example_output": "Min: 1, Max: 9",
        "hint": "Initialize `min` and `max` with `nums[0]`. Loop through the array from index 1 comparing each element.",
        "starter_code": """public class MinMaxFinder {
    public static void findMinMax(int[] nums) {
        // Print Min and Max
    }
}
""",
        "solution": """public class MinMaxFinder {
    public static void findMinMax(int[] nums) {
        if (nums == null || nums.length == 0) return;
        int min = nums[0];
        int max = nums[0];

        for (int i = 1; i < nums.length; i++) {
            if (nums[i] < min) min = nums[i];
            if (nums[i] > max) max = nums[i];
        }
        System.out.println("Min: " + min + ", Max: " + max);
    }
}
""",
        "approach": "1. Guard against empty arrays.\n2. Seed `min = nums[0]` and `max = nums[0]`.\n3. Loop across array updating `min` and `max`.\n4. Print results.",
        "explanation": "A single linear scan determines both boundaries in O(N) operations without sorting.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Check Palindrome String in Java",
        "difficulty": "Beginner",
        "order_index": 23,
        "description": "Write a Java method `boolean isPalindrome(String str)` that checks whether a given string is a palindrome, ignoring uppercase/lowercase differences.",
        "example_input": "\"Madam\"",
        "example_output": "true",
        "hint": "Use two pointers starting at index 0 and `length() - 1`. Compare `Character.toLowerCase()` at each position.",
        "starter_code": """public class PalindromeChecker {
    public static boolean isPalindrome(String str) {
        // Write your solution here
        return false;
    }
}
""",
        "solution": """public class PalindromeChecker {
    public static boolean isPalindrome(String str) {
        if (str == null) return false;
        int left = 0;
        int right = str.length() - 1;

        while (left < right) {
            char cLeft = Character.toLowerCase(str.charAt(left));
            char cRight = Character.toLowerCase(str.charAt(right));
            if (cLeft != cRight) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
""",
        "approach": "1. Initialize two pointers: `left = 0`, `right = str.length() - 1`.\n2. Compare characters after `Character.toLowerCase()`.\n3. If mismatch, return false.\n4. Increment `left`, decrement `right` until crossed.\n5. Return true.",
        "explanation": "Two-pointer comparison operates in-place without creating reversed string objects, saving heap allocation.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Constructor Overloading (Rectangle Class)",
        "difficulty": "Beginner",
        "order_index": 24,
        "description": "Demonstrate constructor overloading in Java by designing a `Rectangle` class with a default constructor (1x1), a square constructor (side), and a rectangle constructor (width, height).",
        "example_input": "new Rectangle(), new Rectangle(5), new Rectangle(4, 6)",
        "example_output": "Areas: 1, 25, 24",
        "hint": "Use constructor chaining `this(...)` to delegate initialization to the most specific constructor.",
        "starter_code": """public class Rectangle {
    private double width;
    private double height;

    // Implement overloaded constructors and getArea()
}
""",
        "solution": """public class Rectangle {
    private double width;
    private double height;

    // Default constructor
    public Rectangle() {
        this(1.0, 1.0);
    }

    // Square constructor
    public Rectangle(double side) {
        this(side, side);
    }

    // Full constructor
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    public double getArea() {
        return this.width * this.height;
    }
}
""",
        "approach": "1. Create full constructor setting width and height.\n2. Overload single-parameter constructor calling `this(side, side)`.\n3. Overload default constructor calling `this(1.0, 1.0)`.\n4. Implement `getArea()`.",
        "explanation": "Constructor overloading allows flexible object instantiation. Chaining through `this()` avoids duplicating initialization logic.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Method Overloading (Calculator Class)",
        "difficulty": "Beginner",
        "order_index": 25,
        "description": "Implement a `Calculator` class with overloaded `add()` methods that can add: (1) two integers, (2) three integers, and (3) two double floating-point numbers.",
        "example_input": "calc.add(2, 3), calc.add(1, 2, 3), calc.add(2.5, 3.5)",
        "example_output": "5, 6, 6.0",
        "hint": "Method overloading requires identical method names with differing parameter types or argument counts.",
        "starter_code": """public class Calculator {
    // Implement overloaded add methods
}
""",
        "solution": """public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }

    public double add(double a, double b) {
        return a + b;
    }
}
""",
        "approach": "1. Define `add(int, int)`.\n2. Overload with `add(int, int, int)`.\n3. Overload with `add(double, double)`.",
        "explanation": "Compile-time polymorphism resolves the target method based on the compile-time type and count of arguments.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Inheritance & Method Overriding (Employee Hierarchy)",
        "difficulty": "Intermediate",
        "order_index": 26,
        "description": "Create a base class `Employee` with field `baseSalary` and method `calculateSalary()`. Create a derived class `Manager` that adds a `bonus` and overrides `calculateSalary()` using `super`.",
        "example_input": "Employee e = new Manager(50000, 15000);",
        "example_output": "65000",
        "hint": "Use the `extends` keyword for inheritance and call `super.calculateSalary() + bonus` in the overriding method.",
        "starter_code": """public class Employee {
    protected double baseSalary;
    // Implement constructor and calculateSalary()
}

class Manager extends Employee {
    private double bonus;
    // Implement constructor and override calculateSalary()
}
""",
        "solution": """public class Employee {
    protected double baseSalary;

    public Employee(double baseSalary) {
        this.baseSalary = baseSalary;
    }

    public double calculateSalary() {
        return this.baseSalary;
    }
}

class Manager extends Employee {
    private double bonus;

    public Manager(double baseSalary, double bonus) {
        super(baseSalary);
        this.bonus = bonus;
    }

    @Override
    public double calculateSalary() {
        return super.calculateSalary() + this.bonus;
    }
}
""",
        "approach": "1. Base class `Employee` provides constructor and `calculateSalary()`.\n2. Derived class `Manager` calls `super(baseSalary)`.\n3. Override `calculateSalary()` adding `bonus`.",
        "explanation": "Method overriding provides runtime polymorphism. `super` invokes the immediate parent's implementation.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Interface Implementation & Polymorphism",
        "difficulty": "Intermediate",
        "order_index": 27,
        "description": "Define an interface `Playable` with method `void play()`. Create classes `Guitar` and `Piano` that implement this interface with specific sound output.",
        "example_input": "Playable p1 = new Guitar(); p1.play();",
        "example_output": "\"Strumming Guitar chords\"",
        "hint": "Use the `interface` keyword and implement it using `implements Playable` in concrete classes.",
        "starter_code": """interface Playable {
    void play();
}

// Implement Guitar and Piano
""",
        "solution": """interface Playable {
    void play();
}

class Guitar implements Playable {
    @Override
    public void play() {
        System.out.println("Strumming Guitar chords");
    }
}

class Piano implements Playable {
    @Override
    public void play() {
        System.out.println("Playing Piano keys");
    }
}
""",
        "approach": "1. Declare `Playable` interface.\n2. Implement `Guitar` with specific `play()` printout.\n3. Implement `Piano` with specific `play()` printout.",
        "explanation": "Interfaces establish a contract for what a class must do without dictating how, enabling decoupled modular architecture.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Custom Exception Handling",
        "difficulty": "Intermediate",
        "order_index": 28,
        "description": "Create a custom checked exception `InvalidAgeException`. Write a method `validateAge(int age)` that throws this exception if `age < 18`.",
        "example_input": "validateAge(16)",
        "example_output": "Throws InvalidAgeException: \"Age must be 18 or older to register\"",
        "hint": "Extend `Exception` for a checked exception or `RuntimeException` for an unchecked exception. Use `throw new InvalidAgeException(...)`.",
        "starter_code": """// Define InvalidAgeException and Validator class
""",
        "solution": """class InvalidAgeException extends Exception {
    public InvalidAgeException(String message) {
        super(message);
    }
}

public class AgeValidator {
    public static void validateAge(int age) throws InvalidAgeException {
        if (age < 18) {
            throw new InvalidAgeException("Age must be 18 or older to register");
        }
        System.out.println("Registration eligible");
    }
}
""",
        "approach": "1. Create class extending `Exception` with message constructor.\n2. In `validateAge`, check condition `age < 18`.\n3. Throw new exception instance if invalid.\n4. Mark method signature with `throws InvalidAgeException`.",
        "explanation": "Custom exceptions clarify application-specific domain errors and force callers to handle failure scenarios gracefully.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Generic Pair Container Class",
        "difficulty": "Advanced",
        "order_index": 29,
        "description": "Implement a generic class `Pair<K, V>` in Java that stores two items of arbitrary types, providing getters, setters, and a string representation.",
        "example_input": "Pair<String, Integer> p = new Pair<>(\"Score\", 95);",
        "example_output": "(Score, 95)",
        "hint": "Use type parameters `<K, V>` in class definition. Store fields of type `K` and `V`.",
        "starter_code": """public class Pair<K, V> {
    // Implement generic Pair
}
""",
        "solution": """public class Pair<K, V> {
    private K key;
    private V value;

    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() { return key; }
    public void setKey(K key) { this.key = key; }

    public V getValue() { return value; }
    public void setValue(V value) { this.value = value; }

    @Override
    public String toString() {
        return "(" + key + ", " + value + ")";
    }
}
""",
        "approach": "1. Declare class with type parameters `<K, V>`.\n2. Store private members `key` and `value`.\n3. Provide getters and setters.\n4. Override `toString()`.",
        "explanation": "Java generics provide compile-time type safety, eliminating type casts and preventing `ClassCastException` at runtime.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Java",
        "category_slug": "java",
        "title": "Thread Synchronization with Bounded Buffer",
        "difficulty": "Advanced",
        "order_index": 30,
        "description": "Implement a thread-safe bounded single-item buffer in Java with synchronized `produce(int value)` and `consume()` methods using `wait()` and `notifyAll()`.",
        "example_input": "Producer thread inserts 42; Consumer thread consumes 42",
        "example_output": "Produced: 42, Consumed: 42",
        "hint": "Always check wait conditions inside a `while` loop (not `if`) to guard against spurious wakeups.",
        "starter_code": """public class BoundedBuffer {
    private int data;
    private boolean hasData = false;

    public synchronized void produce(int value) throws InterruptedException {
        // Implement produce
    }

    public synchronized int consume() throws InterruptedException {
        // Implement consume
        return 0;
    }
}
""",
        "solution": """public class BoundedBuffer {
    private int data;
    private boolean hasData = false;

    public synchronized void produce(int value) throws InterruptedException {
        while (hasData) {
            wait();
        }
        this.data = value;
        this.hasData = true;
        notifyAll();
    }

    public synchronized int consume() throws InterruptedException {
        while (!hasData) {
            wait();
        }
        int result = this.data;
        this.hasData = false;
        notifyAll();
        return result;
    }
}
""",
        "approach": "1. Keep state flag `hasData`.\n2. In `produce`, wait while buffer is full; write data, set flag, notify.\n3. In `consume`, wait while empty; read data, reset flag, notify.\n4. Protect methods with `synchronized` monitor lock.",
        "explanation": "Guarded blocks using `wait()` release the intrinsic monitor lock and suspend execution until signaled, coordinating concurrent threads without busy waiting.",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    },

    # =========================================================================
    # 4. DATA STRUCTURES (10 Questions)
    # =========================================================================
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Array Element Insertion at Index",
        "difficulty": "Beginner",
        "order_index": 31,
        "description": "Given an array of capacity `cap` currently containing `n` elements, write a function to insert an element `val` at index `idx`, shifting subsequent elements to the right.",
        "example_input": "arr = [10, 20, 30, 40], n = 4, idx = 2, val = 25",
        "example_output": "[10, 20, 25, 30, 40]",
        "hint": "Shift elements starting from the rightmost element `arr[n - 1]` down to `arr[idx]` to make space for the new value.",
        "starter_code": """def insert_at_index(arr: list, n: int, idx: int, val: int) -> list:
    # Shift elements right and insert
    pass
""",
        "solution": """def insert_at_index(arr: list, n: int, idx: int, val: int) -> list:
    arr.append(None)
    for i in range(n, idx, -1):
        arr[i] = arr[i - 1]
    arr[idx] = val
    return arr
""",
        "approach": "1. Expand list by one slot.\n2. Shift elements right from index `n` down to `idx + 1`.\n3. Place `val` at index `idx`.\n4. Return array.",
        "explanation": "Inserting into a contiguous array requires shifting all subsequent elements to maintain contiguous ordering.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Singly Linked List Traversal",
        "difficulty": "Beginner",
        "order_index": 32,
        "description": "Define a singly linked list node structure and write a traversal function that collects and prints values from `head` to `null`.",
        "example_input": "1 -> 2 -> 3 -> 4 -> None",
        "example_output": "[1, 2, 3, 4]",
        "hint": "Start with `curr = head`. In a while loop, process `curr.val` and advance `curr = curr.next` until `curr is None`.",
        "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def traverse_list(head: ListNode) -> list:
    # Collect values
    pass
""",
        "solution": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def traverse_list(head: ListNode) -> list:
    values = []
    curr = head
    while curr:
        values.append(curr.val)
        curr = curr.next
    return values
""",
        "approach": "1. Set current pointer to `head`.\n2. While current is not null, record `curr.val`.\n3. Advance `curr = curr.next`.\n4. Return collected list.",
        "explanation": "Unlike arrays, linked lists are stored non-contiguously in memory; traversal requires following pointer links one node at a time.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1) auxiliary"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Stack Implementation Using an Array",
        "difficulty": "Beginner",
        "order_index": 33,
        "description": "Implement a Last-In-First-Out (LIFO) Stack class supporting `push(x)`, `pop()`, `peek()`, `is_empty()`, and `size()`.",
        "example_input": "push(10), push(20), pop(), peek()",
        "example_output": "pop returns 20, peek returns 10",
        "hint": "Use a dynamic array or list where appending acts as `push` and removing the last element acts as `pop`.",
        "starter_code": """class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, val): pass
    def pop(self): pass
    def peek(self): pass
    def is_empty(self) -> bool: pass
    def size(self) -> int: pass
""",
        "solution": """class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, val):
        self._items.append(val)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)
""",
        "approach": "1. Maintain internal list.\n2. `push` appends to tail.\n3. `pop` removes and returns tail.\n4. `peek` inspects index -1.",
        "explanation": "Operating at the end of a dynamic array guarantees amortized O(1) performance for all core stack operations.",
        "time_complexity": "O(1) amortized for all operations",
        "space_complexity": "O(N)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Circular Queue Implementation",
        "difficulty": "Beginner",
        "order_index": 34,
        "description": "Design a First-In-First-Out (FIFO) circular queue with fixed capacity `k` supporting `enqueue()`, `dequeue()`, `front()`, and `is_full()`.",
        "example_input": "enqueue(1), enqueue(2), dequeue(), enqueue(3)",
        "example_output": "Front: 2, Elements: [2, 3]",
        "hint": "Use modulo arithmetic `(tail + 1) % k` to wrap around indices when reaching the end of the backing array.",
        "starter_code": """class MyCircularQueue:
    def __init__(self, k: int):
        # Initialize circular queue
        pass
""",
        "solution": """class MyCircularQueue:
    def __init__(self, k: int):
        self.capacity = k
        self.queue = [0] * k
        self.head = 0
        self.tail = -1
        self.size = 0

    def enqueue(self, value: int) -> bool:
        if self.is_full():
            return False
        self.tail = (self.tail + 1) % self.capacity
        self.queue[self.tail] = value
        self.size += 1
        return True

    def dequeue(self) -> bool:
        if self.is_empty():
            return False
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return True

    def front(self) -> int:
        return -1 if self.is_empty() else self.queue[self.head]

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        return self.size == self.capacity
""",
        "approach": "1. Track `head`, `tail`, and `size`.\n2. On enqueue, advance `tail = (tail + 1) % capacity`.\n3. On dequeue, advance `head = (head + 1) % capacity`.\n4. Modulo arithmetic wraps indices continuously.",
        "explanation": "A circular queue reuses vacated array slots at the front of the buffer without shifting remaining elements.",
        "time_complexity": "O(1) for all operations",
        "space_complexity": "O(K)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Find the Middle Element of a Linked List",
        "difficulty": "Intermediate",
        "order_index": 35,
        "description": "Given the `head` of a singly linked list, return the middle node. If there are two middle nodes, return the second middle node.",
        "example_input": "head = [1, 2, 3, 4, 5]",
        "example_output": "Node with value 3",
        "hint": "Use Floyd's fast and slow pointer technique: advance `slow` by 1 step and `fast` by 2 steps in each iteration.",
        "starter_code": """def find_middle_node(head):
    # Two-pointer tortoise and hare
    pass
""",
        "solution": """def find_middle_node(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
""",
        "approach": "1. Initialize `slow = head` and `fast = head`.\n2. In loop, advance `slow` by 1 node and `fast` by 2 nodes.\n3. When `fast` reaches end or null, `slow` is exactly at the midpoint.\n4. Return `slow`.",
        "explanation": "Because `fast` travels at twice the speed of `slow`, when `fast` finishes traversing the list, `slow` must be at the halfway mark in a single pass.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Reverse a Singly Linked List",
        "difficulty": "Intermediate",
        "order_index": 36,
        "description": "Given the head of a singly linked list, reverse the list iteratively and return the new head pointer.",
        "example_input": "1 -> 2 -> 3 -> 4 -> None",
        "example_output": "4 -> 3 -> 2 -> 1 -> None",
        "hint": "Maintain three pointers: `prev = None`, `curr = head`, and `next_node`. Point `curr.next` to `prev` and slide pointers forward.",
        "starter_code": """def reverse_linked_list(head):
    # Iterative pointer reversal
    pass
""",
        "solution": """def reverse_linked_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
""",
        "approach": "1. Start with `prev = None` and `curr = head`.\n2. Save `next_node = curr.next`.\n3. Reverse direction: `curr.next = prev`.\n4. Advance `prev = curr` and `curr = next_node`.\n5. When loop terminates, `prev` is the new head.",
        "explanation": "Modifying next pointers in-place reverses the entire list in O(N) operations using zero extra heap memory.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Check Balanced Parentheses Using Stack",
        "difficulty": "Intermediate",
        "order_index": 37,
        "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid (brackets close in the correct order).",
        "example_input": "s = \"{[()]}\"",
        "example_output": "True",
        "hint": "Push opening brackets onto a stack. When a closing bracket is encountered, verify that the top of the stack matches its corresponding pair.",
        "starter_code": """def is_valid_parentheses(s: str) -> bool:
    # Use stack
    pass
""",
        "solution": """def is_valid_parentheses(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)

    return len(stack) == 0
""",
        "approach": "1. Create mapping of closing brackets to opening brackets.\n2. Iterate through characters.\n3. If closing bracket, pop from stack and check match.\n4. If opening bracket, push to stack.\n5. Return True if stack is completely empty.",
        "explanation": "A LIFO stack matches the most recently opened bracket with the first encountered closing bracket.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Binary Search Tree Insertion and Inorder Traversal",
        "difficulty": "Intermediate",
        "order_index": 38,
        "description": "Implement node insertion into a Binary Search Tree (BST) maintaining the property that left children are smaller and right children are larger. Perform an inorder traversal returning values in sorted order.",
        "example_input": "Insert [5, 3, 7, 2, 4]",
        "example_output": "Inorder traversal: [2, 3, 4, 5, 7]",
        "hint": "If insertion value is smaller than current node, traverse left; if larger, traverse right. Inorder traversal visits Left, Root, Right.",
        "starter_code": """class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def insert_bst(root, val): pass
def inorder_traversal(root): pass
""",
        "solution": """class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def insert_bst(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root

def inorder_traversal(root):
    res = []
    def _inorder(node):
        if not node: return
        _inorder(node.left)
        res.append(node.val)
        _inorder(node.right)
    _inorder(root)
    return res
""",
        "approach": "1. In `insert_bst`, compare `val` to current node to decide left or right branch.\n2. In `inorder_traversal`, visit Left subtree, append Root value, visit Right subtree.",
        "explanation": "Inorder traversal of any valid BST naturally produces elements in non-decreasing sorted order.",
        "time_complexity": "O(H) insertion where H is height, O(N) traversal",
        "space_complexity": "O(H) recursion stack"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Detect Cycle in a Linked List (Floyd's Algorithm)",
        "difficulty": "Advanced",
        "order_index": 39,
        "description": "Given the `head` of a linked list, determine if the linked list has a cycle in it without using extra memory for a hash table.",
        "example_input": "Node 3 -> 2 -> 0 -> -4 (points back to Node 2)",
        "example_output": "True",
        "hint": "If a cycle exists, a fast pointer moving 2 steps will eventually lap and collide with a slow pointer moving 1 step.",
        "starter_code": """def has_cycle(head) -> bool:
    # Floyd's cycle-finding algorithm
    pass
""",
        "solution": """def has_cycle(head) -> bool:
    if not head or not head.next:
        return False
    slow = head
    fast = head.next
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    return True
""",
        "approach": "1. Initialize `slow = head` and `fast = head.next`.\n2. In while loop, check if `slow == fast` (collision).\n3. Advance `slow` by 1 and `fast` by 2.\n4. If `fast` hits `None`, no cycle exists.",
        "explanation": "In a closed loop of length C, the relative distance between the two pointers decreases by 1 step in each iteration, guaranteeing collision within O(N) steps.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "Data Structures",
        "category_slug": "data-structures",
        "title": "Binary Tree Level Order Traversal (BFS)",
        "difficulty": "Advanced",
        "order_index": 40,
        "description": "Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level as a list of lists).",
        "example_input": "root = [3, 9, 20, None, None, 15, 7]",
        "example_output": "[[3], [9, 20], [15, 7]]",
        "hint": "Use a FIFO queue. Record the size of the queue at the start of each level to process nodes level by level.",
        "starter_code": """from collections import deque

def level_order(root) -> list[list[int]]:
    # Breadth-first search queue
    pass
""",
        "solution": """from collections import deque

def level_order(root) -> list[list[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)

    return result
""",
        "approach": "1. Initialize queue with `root`.\n2. In while loop, capture `level_size = len(queue)`.\n3. Dequeue `level_size` nodes, collecting their values and enqueueing their children.\n4. Append level list to result.",
        "explanation": "Breadth-First Search processes all neighbors at distance d before moving to distance d+1, yielding clean hierarchical level partitions.",
        "time_complexity": "O(N)",
        "space_complexity": "O(W) where W is maximum width of tree"
    },

    # =========================================================================
    # 5. DSA (DATA STRUCTURES & ALGORITHMS) (10 Questions)
    # =========================================================================
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Linear Search Algorithm",
        "difficulty": "Beginner",
        "order_index": 41,
        "description": "Implement the Linear Search algorithm to find the index of a target value in an unsorted list. Return the 0-based index if found, or -1 if the target does not exist.",
        "example_input": "arr = [4, 2, 7, 1, 9], target = 7",
        "example_output": "2",
        "hint": "Iterate sequentially through each index using `enumerate(arr)` and compare with `target`.",
        "starter_code": """def linear_search(arr: list[int], target: int) -> int:
    # Sequential scan
    pass
""",
        "solution": """def linear_search(arr: list[int], target: int) -> int:
    for idx, val in enumerate(arr):
        if val == target:
            return idx
    return -1
""",
        "approach": "1. Loop through array inspecting each element.\n2. If current element matches `target`, return its index.\n3. If loop finishes without match, return -1.",
        "explanation": "Linear search is the simplest search algorithm, requiring no sorting or prior assumptions about data ordering.",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Binary Search on a Sorted Array",
        "difficulty": "Beginner",
        "order_index": 42,
        "description": "Given a sorted array of distinct integers `nums` and a target value `target`, write a function to search `target` in `nums` with O(log N) runtime complexity.",
        "example_input": "nums = [-1, 0, 3, 5, 9, 12], target = 9",
        "example_output": "4",
        "hint": "Compute `mid = low + (high - low) // 2`. If `nums[mid] == target` return mid; if smaller, search right; if larger, search left.",
        "starter_code": """def binary_search(nums: list[int], target: int) -> int:
    # Logarithmic search
    pass
""",
        "solution": """def binary_search(nums: list[int], target: int) -> int:
    low = 0
    high = len(nums) - 1

    while low <= high:
        mid = low + (high - low) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
""",
        "approach": "1. Set pointers `low = 0` and `high = len - 1`.\n2. While `low <= high`, calculate `mid`.\n3. Compare `nums[mid]` to `target`.\n4. Halve the search space based on comparison.",
        "explanation": "Halving the search space in each iteration yields O(log N) efficiency, searching 1 billion items in at most 30 comparisons.",
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Bubble Sort with Early Exit Optimization",
        "difficulty": "Beginner",
        "order_index": 43,
        "description": "Implement Bubble Sort to sort an array in ascending order. Add an early-exit optimization flag that stops execution if the array is already sorted.",
        "example_input": "arr = [64, 34, 25, 12, 22, 11, 90]",
        "example_output": "[11, 12, 22, 25, 34, 64, 90]",
        "hint": "Use a boolean `swapped` flag in the outer loop. If no two elements were swapped in a complete pass, break early.",
        "starter_code": """def bubble_sort(arr: list[int]) -> list[int]:
    # Optimized bubble sort
    pass
""",
        "solution": """def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
""",
        "approach": "1. Iterate `i` from 0 to n-1.\n2. In inner loop, compare adjacent elements `arr[j]` and `arr[j+1]`.\n3. Swap if out of order and set `swapped = True`.\n4. If `not swapped`, terminate early.",
        "explanation": "With the `swapped` flag, Bubble Sort detects already-sorted inputs in best-case O(N) time.",
        "time_complexity": "O(N^2) average/worst, O(N) best case",
        "space_complexity": "O(1)"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Recursive Power Calculation (x^n)",
        "difficulty": "Beginner",
        "order_index": 44,
        "description": "Implement a function `power(x: float, n: int) -> float` to calculate `x` raised to the power `n` using recursive binary exponentiation.",
        "example_input": "x = 2.0, n = 10",
        "example_output": "1024.0",
        "hint": "If n is even, `x^n = (x^(n/2))^2`. If n is odd, `x^n = x * x^(n-1)`. Handle base case `n == 0`.",
        "starter_code": """def my_pow(x: float, n: int) -> float:
    # Binary exponentiation
    pass
""",
        "solution": """def my_pow(x: float, n: int) -> float:
    if n == 0:
        return 1.0
    if n < 0:
        return 1.0 / my_pow(x, -n)

    half = my_pow(x, n // 2)
    if n % 2 == 0:
        return half * half
    else:
        return half * half * x
""",
        "approach": "1. Base case: `n == 0` returns 1.0.\n2. If `n < 0`, return `1.0 / my_pow(x, -n)`.\n3. Recursively compute `half = my_pow(x, n // 2)`.\n4. If even, return `half * half`; if odd, multiply by `x`.",
        "explanation": "Binary exponentiation reduces multiplication steps from O(N) to O(log N) by squaring intermediate powers.",
        "time_complexity": "O(log N)",
        "space_complexity": "O(log N) stack depth"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Merge Sort Algorithm",
        "difficulty": "Intermediate",
        "order_index": 45,
        "description": "Implement the divide-and-conquer Merge Sort algorithm to sort an array of numbers in ascending order.",
        "example_input": "arr = [38, 27, 43, 3, 9, 82, 10]",
        "example_output": "[3, 9, 10, 27, 38, 43, 82]",
        "hint": "Recursively divide the array at the midpoint into two halves until length is 1, then merge the two sorted halves.",
        "starter_code": """def merge_sort(arr: list[int]) -> list[int]:
    # Divide and conquer
    pass
""",
        "solution": """def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge step
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
""",
        "approach": "1. Base case: array with length <= 1 is already sorted.\n2. Divide: split into `left` and `right` sub-arrays.\n3. Conquer: recursively sort each half.\n4. Combine: merge two sorted arrays using two pointers.",
        "explanation": "Merge sort guarantees stable O(N log N) sorting across worst, average, and best cases.",
        "time_complexity": "O(N log N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Quick Sort Algorithm",
        "difficulty": "Intermediate",
        "order_index": 46,
        "description": "Implement the Quick Sort algorithm using an in-place partition scheme (Lomuto partition) choosing the last element as the pivot.",
        "example_input": "arr = [10, 80, 30, 90, 40, 50, 70]",
        "example_output": "[10, 30, 40, 50, 70, 80, 90]",
        "hint": "Partition elements smaller than the pivot to the left, and elements greater to the right, then recursively sort partitions.",
        "starter_code": """def quick_sort(arr: list[int], low: int, high: int):
    # In-place partition quick sort
    pass
""",
        "solution": """def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr: list[int], low: int = 0, high: int = None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr
""",
        "approach": "1. Select pivot (e.g. `arr[high]`).\n2. Partition elements so items <= pivot are on left.\n3. Place pivot at boundary index `i + 1`.\n4. Recursively sort left and right sub-arrays.",
        "explanation": "Quick Sort is typically the fastest general-purpose in-memory sorting algorithm in practice due to excellent cache locality.",
        "time_complexity": "O(N log N) average, O(N^2) worst case",
        "space_complexity": "O(log N) stack space"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Two Sum Problem (Hashing Technique)",
        "difficulty": "Intermediate",
        "order_index": 47,
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.",
        "example_input": "nums = [2, 7, 11, 15], target = 9",
        "example_output": "[0, 1]",
        "hint": "Store each number's index in a hash map. For current number `x`, check if complement `target - x` has already been seen.",
        "starter_code": """def two_sum(nums: list[int], target: int) -> list[int]:
    # Hash map complement lookup
    pass
""",
        "solution": """def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], idx]
        seen[num] = idx
    return []
""",
        "approach": "1. Initialize hash map `seen`.\n2. Iterate through `nums` with indices.\n3. Compute `complement = target - num`.\n4. If complement in `seen`, return `[seen[complement], idx]`.\n5. Otherwise record `seen[num] = idx`.",
        "explanation": "Hashing reduces the brute-force O(N^2) search down to a single O(N) pass by transforming searching into constant-time key lookup.",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Breadth-First Search (BFS) on Graph",
        "difficulty": "Intermediate",
        "order_index": 48,
        "description": "Implement Breadth-First Search on an undirected graph represented as an adjacency list. Return the traversal order starting from a source node.",
        "example_input": "graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}, start = 0",
        "example_output": "[0, 1, 2, 3, 4]",
        "hint": "Use a FIFO queue and a `visited` set to prevent infinite loops in cyclic graphs.",
        "starter_code": """from collections import deque

def bfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:
    # Queue-based traversal
    pass
""",
        "solution": """from collections import deque

def bfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:
    visited = set([start])
    queue = deque([start])
    traversal = []

    while queue:
        vertex = queue.popleft()
        traversal.append(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal
""",
        "approach": "1. Enqueue `start` and add to `visited` set.\n2. While queue is not empty, pop head `vertex` and record.\n3. For each unvisited neighbor, mark visited and enqueue.\n4. Return traversal order.",
        "explanation": "BFS explores graph nodes in order of shortest distance from the source, making it ideal for shortest-path finding on unweighted graphs.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "Depth-First Search (DFS) on Graph",
        "difficulty": "Advanced",
        "order_index": 49,
        "description": "Implement Depth-First Search on a graph to discover all connected nodes starting from a source vertex, using recursive or stack-based traversal.",
        "example_input": "graph = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}, start = 0",
        "example_output": "[0, 1, 3, 2, 4]",
        "hint": "Visit deep into branches as far as possible before backtracking. Use a `visited` set to track traversed vertices.",
        "starter_code": """def dfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:
    # Recursive DFS
    pass
""",
        "solution": """def dfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:
    visited = set()
    order = []

    def _dfs(node):
        visited.add(node)
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return order
""",
        "approach": "1. Maintain `visited` set and `order` list.\n2. In helper `_dfs(node)`, add to visited and order.\n3. Iterate neighbors; if not visited, recurse immediately.\n4. Backtrack naturally as calls return.",
        "explanation": "DFS explores deep into paths before backtracking, fundamental for topological sorting, cycle detection, and strongly connected components.",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V) call stack"
    },
    {
        "category": "DSA",
        "category_slug": "dsa",
        "title": "0/1 Knapsack Problem (Dynamic Programming)",
        "difficulty": "Advanced",
        "order_index": 50,
        "description": "Given weights `weights` and values `values` of `n` items, find the maximum value that can be placed in a knapsack of capacity `W`. Each item can either be taken (1) or left (0).",
        "example_input": "values = [60, 100, 120], weights = [10, 20, 30], W = 50",
        "example_output": "220",
        "hint": "Build a 2D table `dp[i][w]` where cell represents max value using first `i` items with max weight `w`.",
        "starter_code": """def knapsack(values: list[int], weights: list[int], W: int) -> int:
    # 0/1 Knapsack Dynamic Programming
    pass
""",
        "solution": """def knapsack(values: list[int], weights: list[int], W: int) -> int:
    n = len(values)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][W]
""",
        "approach": "1. Initialize 2D table `dp[n+1][W+1]` with 0s.\n2. Outer loop `i` over items, inner loop `w` over capacities.\n3. If item fits, choose `max(exclude item, include item + value)`.\n4. If item exceeds `w`, exclude it.\n5. Answer is in `dp[n][W]`.",
        "explanation": "Dynamic programming avoids overlapping subproblem re-computations by caching intermediate optimal solutions in a table.",
        "time_complexity": "O(N * W)",
        "space_complexity": "O(N * W)"
    }
]

