// SkillPath Resilient Offline & Vercel Mock Data
// Provides instant zero-latency experience when viewing preview or when backend is connecting

export const MOCK_CATEGORIES = [
  {
    "id": "c-programming",
    "name": "C Programming",
    "description": "Practice fundamentals including variables, loops, functions, arrays and pointers.",
    "question_count": 10,
    "difficulty_counts": {
      "Beginner": 4,
      "Intermediate": 4,
      "Advanced": 2
    },
    "completed_count": 0,
    "icon": "Terminal"
  },
  {
    "id": "python",
    "name": "Python",
    "description": "Practice Python syntax, functions, lists, dictionaries and problem-solving.",
    "question_count": 10,
    "difficulty_counts": {
      "Beginner": 4,
      "Intermediate": 4,
      "Advanced": 2
    },
    "completed_count": 0,
    "icon": "Code"
  },
  {
    "id": "java",
    "name": "Java",
    "description": "Practice object-oriented programming, classes, inheritance and core Java concepts.",
    "question_count": 10,
    "difficulty_counts": {
      "Beginner": 4,
      "Intermediate": 4,
      "Advanced": 2
    },
    "completed_count": 0,
    "icon": "FileCode"
  },
  {
    "id": "data-structures",
    "name": "Data Structures",
    "description": "Practice arrays, linked lists, stacks, queues, trees and graphs.",
    "question_count": 10,
    "difficulty_counts": {
      "Beginner": 4,
      "Intermediate": 4,
      "Advanced": 2
    },
    "completed_count": 0,
    "icon": "Layers"
  },
  {
    "id": "dsa",
    "name": "DSA",
    "description": "Practice algorithms including searching, sorting, recursion, dynamic programming and problem-solving.",
    "question_count": 10,
    "difficulty_counts": {
      "Beginner": 3,
      "Intermediate": 4,
      "Advanced": 3
    },
    "completed_count": 0,
    "icon": "Cpu"
  }
];

export const MOCK_QUESTIONS = [
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
    "starter_code": "#include <stdio.h>\n\nlong long reverseNumber(long long n) {\n    // Write your solution here\n    return 0;\n}\n\nint main() {\n    long long n = 12345;\n    printf(\"Reversed: %lld\\n\", reverseNumber(n));\n    return 0;\n}\n",
    "solution": "#include <stdio.h>\n\nlong long reverseNumber(long long n) {\n    long long reversed = 0;\n    while (n > 0) {\n        int remainder = n % 10;\n        reversed = reversed * 10 + remainder;\n        n /= 10;\n    }\n    return reversed;\n}\n\nint main() {\n    long long n = 12345;\n    printf(\"Reversed: %lld\\n\", reverseNumber(n));\n    return 0;\n}\n",
    "approach": "1. Initialize `reversed` to 0.\n2. In a loop while `n > 0`, extract the units digit with `remainder = n % 10`.\n3. Shift `reversed` left by multiplying by 10 and add the remainder.\n4. Truncate `n` by dividing by 10.\n5. Return `reversed`.",
    "explanation": "Modulo by 10 isolates the least-significant digit. Multiplying the accumulator by 10 shifts existing digits one place to the left, correctly assembling the reversed number from left to right.",
    "time_complexity": "O(log10(N))",
    "space_complexity": "O(1)",
    "id": 1,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n#include <stdbool.h>\n\nbool isPrime(int n) {\n    // Write your code here\n    return false;\n}\n",
    "solution": "#include <stdio.h>\n#include <stdbool.h>\n\nbool isPrime(int n) {\n    if (n <= 1) return false;\n    if (n <= 3) return true;\n    if (n % 2 == 0 || n % 3 == 0) return false;\n\n    for (int i = 5; i * i <= n; i += 6) {\n        if (n % i == 0 || n % (i + 2) == 0)\n            return false;\n    }\n    return true;\n}\n",
    "approach": "1. Guard against numbers <= 1.\n2. Handle 2 and 3 as initial primes.\n3. Eliminate even numbers and multiples of 3.\n4. Check divisibility up to `sqrt(n)` using step increments of 6 (checking `i` and `i + 2`).",
    "explanation": "All primes greater than 3 can be expressed in the form 6k \u00b1 1. Checking up to the square root reduces unnecessary iterations from O(N) to O(sqrt(N)).",
    "time_complexity": "O(sqrt(N))",
    "space_complexity": "O(1)",
    "id": 2,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n\nint findMax(int arr[], int n) {\n    // Return largest integer\n    return 0;\n}\n",
    "solution": "#include <stdio.h>\n\nint findMax(int arr[], int n) {\n    if (n <= 0) return -1;\n    int maxVal = arr[0];\n    for (int i = 1; i < n; i++) {\n        if (arr[i] > maxVal) {\n            maxVal = arr[i];\n        }\n    }\n    return maxVal;\n}\n",
    "approach": "1. Set `maxVal = arr[0]`.\n2. Iterate through indices 1 to n-1.\n3. If `arr[i] > maxVal`, update `maxVal = arr[i]`.\n4. Return `maxVal`.",
    "explanation": "A single linear pass inspects every element once to guarantee finding the true maximum.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 3,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n#include <stdbool.h>\n\nbool isPalindrome(int x) {\n    // Write your code here\n    return false;\n}\n",
    "solution": "#include <stdio.h>\n#include <stdbool.h>\n\nbool isPalindrome(int x) {\n    if (x < 0) return false;\n    long long original = x;\n    long long reversed = 0;\n    while (x > 0) {\n        reversed = reversed * 10 + (x % 10);\n        x /= 10;\n    }\n    return original == reversed;\n}\n",
    "approach": "1. Return false if x < 0.\n2. Store copy of original number.\n3. Reverse digits using `% 10` and `/ 10`.\n4. Return comparison `original == reversed`.",
    "explanation": "Reversing the number and testing equality with the preserved original confirms whether symmetry holds.",
    "time_complexity": "O(log10(N))",
    "space_complexity": "O(1)",
    "id": 4,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n\nvoid printFibonacci(int n) {\n    // Print first n Fibonacci numbers\n}\n",
    "solution": "#include <stdio.h>\n\nvoid printFibonacci(int n) {\n    if (n <= 0) return;\n    long long first = 0, second = 1;\n    for (int i = 0; i < n; i++) {\n        printf(\"%lld \", first);\n        long long next = first + second;\n        first = second;\n        second = next;\n    }\n    printf(\"\\n\");\n}\n",
    "approach": "1. Check edge case `n <= 0`.\n2. Print `first`.\n3. Calculate `next = first + second`.\n4. Shift `first = second` and `second = next`.\n5. Repeat `n` times.",
    "explanation": "Iterative Fibonacci avoids the exponential O(2^N) overhead of naive recursion by keeping only the last two computed terms.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 5,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n\nvoid swap(int *a, int *b) {\n    // Swap values through dereferenced pointers\n}\n",
    "solution": "#include <stdio.h>\n\nvoid swap(int *a, int *b) {\n    if (a == NULL || b == NULL) return;\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}\n",
    "approach": "1. Verify pointers are not NULL.\n2. Store value pointed to by `a` into temporary variable `temp`.\n3. Assign value pointed to by `b` into memory at `*a`.\n4. Assign `temp` into memory at `*b`.",
    "explanation": "In C, function arguments are passed by value. Passing addresses via pointers allows the function to directly modify variables in the caller's stack frame.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 6,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n#include <ctype.h>\n\nvoid countVowelsConsonants(const char *str, int *vowels, int *consonants) {\n    // Write your code here\n}\n",
    "solution": "#include <stdio.h>\n#include <ctype.h>\n\nvoid countVowelsConsonants(const char *str, int *vowels, int *consonants) {\n    *vowels = 0;\n    *consonants = 0;\n    while (*str) {\n        char c = tolower(*str);\n        if (c >= 'a' && c <= 'z') {\n            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {\n                (*vowels)++;\n            } else {\n                (*consonants)++;\n            }\n        }\n        str++;\n    }\n}\n",
    "approach": "1. Reset counts to 0.\n2. Traverse characters using pointer increment until `\\0`.\n3. Check if character is alphabetic.\n4. Increment vowel count if matched with 'a', 'e', 'i', 'o', 'u', otherwise consonant count.",
    "explanation": "Traversing through pointer dereferencing `*str` until the null terminator allows linear O(N) evaluation with zero memory allocations.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 7,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n#include <stdlib.h>\n\nlong long sumOfSquares(int n) {\n    // Allocate dynamically, sum, and free\n    return 0;\n}\n",
    "solution": "#include <stdio.h>\n#include <stdlib.h>\n\nlong long sumOfSquares(int n) {\n    if (n <= 0) return 0;\n    int *arr = (int *)malloc(n * sizeof(int));\n    if (arr == NULL) {\n        return -1; // Allocation failure\n    }\n\n    long long sum = 0;\n    for (int i = 0; i < n; i++) {\n        arr[i] = i * i;\n        sum += arr[i];\n    }\n\n    free(arr);\n    arr = NULL;\n    return sum;\n}\n",
    "approach": "1. Allocate heap memory: `malloc(n * sizeof(int))`.\n2. Guard against allocation failure.\n3. Compute values and accumulate sum.\n4. Free memory with `free(arr)` and set pointer to NULL.",
    "explanation": "Dynamic memory management is central to C. Allocating on the heap avoids stack overflow for large datasets, but requires strict deallocation to prevent memory leaks.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 8,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n#include <string.h>\n\nvoid reverseStringInPlace(char *str) {\n    // In-place pointer swap\n}\n",
    "solution": "#include <stdio.h>\n#include <string.h>\n\nvoid reverseStringInPlace(char *str) {\n    if (str == NULL || *str == '\\0') return;\n    char *start = str;\n    char *end = str + strlen(str) - 1;\n\n    while (start < end) {\n        char temp = *start;\n        *start = *end;\n        *end = temp;\n        start++;\n        end--;\n    }\n}\n",
    "approach": "1. Point `start` to head of string.\n2. Point `end` to `str + len - 1`.\n3. Swap `*start` and `*end`.\n4. Increment `start`, decrement `end`.\n5. Terminate when pointers cross.",
    "explanation": "The two-pointer technique achieves in-place reversal in O(N/2) swaps with strict O(1) auxiliary space.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 9,
    "status": "unattempted"
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
    "starter_code": "#include <stdio.h>\n\nsize_t my_strlen(const char *str) {\n    // Write your code here\n    return 0;\n}\n\nchar *my_strcpy(char *dest, const char *src) {\n    // Write your code here\n    return dest;\n}\n",
    "solution": "#include <stdio.h>\n\nsize_t my_strlen(const char *str) {\n    const char *ptr = str;\n    while (*ptr != '\\0') {\n        ptr++;\n    }\n    return (size_t)(ptr - str);\n}\n\nchar *my_strcpy(char *dest, const char *src) {\n    char *d = dest;\n    while ((*d++ = *src++) != '\\0') {\n        // Copy until null byte\n    }\n    return dest;\n}\n",
    "approach": "1. In `my_strlen`, advance `ptr` to null byte; the difference `ptr - str` equals length.\n2. In `my_strcpy`, assign each character from source to destination including the closing `\\0`.\n3. Return destination pointer.",
    "explanation": "Demonstrates low-level pointer arithmetic and idiomatic C copy idiom `while((*d++ = *src++))`, fundamental to systems programming.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 10,
    "status": "unattempted"
  },
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
    "starter_code": "def reverse_string(s: str) -> str:\n    # Write your solution here\n    pass\n",
    "solution": "def reverse_string(s: str) -> str:\n    return s[::-1]\n",
    "approach": "1. Use Python's built-in sequence slicing `s[::-1]`.\n2. Slicing with a step of `-1` starts at the end and steps backward to the beginning.",
    "explanation": "Python string slicing is implemented in C under the hood, making `s[::-1]` both the most idiomatic and fastest way to reverse strings in Python.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 11,
    "status": "unattempted"
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
    "starter_code": "def char_frequency(s: str) -> dict[str, int]:\n    # Write your solution here\n    pass\n",
    "solution": "def char_frequency(s: str) -> dict[str, int]:\n    freq = {}\n    for char in s:\n        freq[char] = freq.get(char, 0) + 1\n    return freq\n",
    "approach": "1. Create an empty dictionary `freq`.\n2. Iterate through each character in the string.\n3. Increment count using `dict.get(char, 0) + 1`.\n4. Return the resulting dictionary.",
    "explanation": "Dictionary key lookups in Python operate in amortized O(1) time via hash tables. A single pass over N characters yields O(N) overall runtime.",
    "time_complexity": "O(N)",
    "space_complexity": "O(K) where K is number of unique characters",
    "id": 12,
    "status": "unattempted"
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
    "starter_code": "def find_duplicates(items: list) -> list:\n    # Write your solution here\n    pass\n",
    "solution": "def find_duplicates(items: list) -> list:\n    seen = set()\n    duplicates = set()\n    for item in items:\n        if item in seen:\n            duplicates.add(item)\n        else:\n            seen.add(item)\n    return list(duplicates)\n",
    "approach": "1. Initialize two sets: `seen` and `duplicates`.\n2. For each element in list, check if present in `seen`.\n3. If present, add to `duplicates`.\n4. Otherwise, add to `seen`.\n5. Convert `duplicates` set to list and return.",
    "explanation": "Set membership checking is O(1) on average. Using sets ensures we collect duplicates efficiently without duplicate listings.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 13,
    "status": "unattempted"
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
    "starter_code": "def is_anagram(s1: str, s2: str) -> bool:\n    # Write your solution here\n    pass\n",
    "solution": "from collections import Counter\n\ndef is_anagram(s1: str, s2: str) -> bool:\n    clean_s1 = s1.replace(\" \", \"\").lower()\n    clean_s2 = s2.replace(\" \", \"\").lower()\n    return Counter(clean_s1) == Counter(clean_s2)\n",
    "approach": "1. Strip spaces and normalize to lowercase.\n2. If string lengths differ, immediately return False.\n3. Count frequencies using `Counter` and compare mappings.",
    "explanation": "Counting frequencies using hash tables is O(N) time and handles unicode characters accurately.",
    "time_complexity": "O(N)",
    "space_complexity": "O(K)",
    "id": 14,
    "status": "unattempted"
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
    "starter_code": "def square_evens(nums: list[int]) -> list[int]:\n    # Return list comprehension\n    pass\n",
    "solution": "def square_evens(nums: list[int]) -> list[int]:\n    return [x ** 2 for x in nums if x % 2 == 0]\n",
    "approach": "1. Iterate through elements with `for x in nums`.\n2. Add filter condition `if x % 2 == 0`.\n3. Transform output expression to `x ** 2`.",
    "explanation": "List comprehensions in Python combine map and filter into concise, optimized bytecode executed faster than manual loop appends.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 15,
    "status": "unattempted"
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
    "starter_code": "from collections import defaultdict\n\ndef group_by(items: list, key_fn) -> dict:\n    # Group items into dictionary\n    pass\n",
    "solution": "from collections import defaultdict\n\ndef group_by(items: list, key_fn) -> dict:\n    grouped = defaultdict(list)\n    for item in items:\n        key = key_fn(item)\n        grouped[key].append(item)\n    return dict(grouped)\n",
    "approach": "1. Instantiate `defaultdict(list)`.\n2. For each item, evaluate `key = key_fn(item)`.\n3. Append item to `grouped[key]`.\n4. Convert to standard dict and return.",
    "explanation": "`defaultdict` streamlines the grouping pattern by executing a factory function whenever a key is first accessed, preventing `KeyError`.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 16,
    "status": "unattempted"
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
    "starter_code": "def merge_sum_dicts(d1: dict, d2: dict) -> dict:\n    # Write your solution here\n    pass\n",
    "solution": "def merge_sum_dicts(d1: dict, d2: dict) -> dict:\n    merged = dict(d1)\n    for k, v in d2.items():\n        merged[k] = merged.get(k, 0) + v\n    return merged\n",
    "approach": "1. Shallow copy `d1` to `merged`.\n2. Loop through `d2.items()`.\n3. Set `merged[k] = merged.get(k, 0) + v`.\n4. Return `merged`.",
    "explanation": "Iterating through the second dictionary updates overlapping keys in O(1) average lookup time per key.",
    "time_complexity": "O(len(d1) + len(d2))",
    "space_complexity": "O(len(d1) + len(d2))",
    "id": 17,
    "status": "unattempted"
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
    "starter_code": "def flatten(nested_list: list) -> list:\n    # Flatten recursively\n    pass\n",
    "solution": "def flatten(nested_list: list) -> list:\n    flat = []\n    for item in nested_list:\n        if isinstance(item, list):\n            flat.extend(flatten(item))\n        else:\n            flat.append(item)\n    return flat\n",
    "approach": "1. Create an output list `flat`.\n2. Iterate through `nested_list`.\n3. If item is an instance of `list`, recursively call `flatten(item)` and extend.\n4. Otherwise append scalar item.\n5. Return `flat`.",
    "explanation": "Recursive traversal visits every terminal scalar exactly once regardless of nesting depth.",
    "time_complexity": "O(Total elements)",
    "space_complexity": "O(Maximum depth + output size)",
    "id": 18,
    "status": "unattempted"
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
    "starter_code": "from typing import Generator\n\ndef generate_primes(limit: int) -> Generator[int, None, None]:\n    # Yield primes lazily\n    pass\n",
    "solution": "from typing import Generator\n\ndef generate_primes(limit: int) -> Generator[int, None, None]:\n    if limit < 2:\n        return\n    is_prime = [True] * (limit + 1)\n    is_prime[0] = is_prime[1] = False\n\n    for num in range(2, limit + 1):\n        if is_prime[num]:\n            yield num\n            for multiple in range(num * num, limit + 1, num):\n                is_prime[multiple] = False\n",
    "approach": "1. Initialize boolean table of size `limit + 1` to True.\n2. Mark 0 and 1 as False.\n3. For each number from 2 to limit, if True, yield the number.\n4. Strike out multiples starting from `num * num` with step `num`.",
    "explanation": "Starting composite marking at `num * num` avoids redundant work. Generators allow memory-friendly streaming of computed primes.",
    "time_complexity": "O(N log(log N))",
    "space_complexity": "O(N)",
    "id": 19,
    "status": "unattempted"
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
    "starter_code": "from collections import OrderedDict\nfrom functools import wraps\n\ndef lru_cache(capacity: int = 3):\n    # Return decorator\n    pass\n",
    "solution": "from collections import OrderedDict\nfrom functools import wraps\n\ndef lru_cache(capacity: int = 3):\n    def decorator(func):\n        cache = OrderedDict()\n        @wraps(func)\n        def wrapper(*args, **kwargs):\n            key = (args, tuple(sorted(kwargs.items())))\n            if key in cache:\n                cache.move_to_end(key)\n                return cache[key]\n            result = func(*args, **kwargs)\n            cache[key] = result\n            if len(cache) > capacity:\n                cache.popitem(last=False)\n            return result\n        return wrapper\n    return decorator\n",
    "approach": "1. Create closure around `OrderedDict`.\n2. Hash arguments into a cache key tuple.\n3. If cache hit, mark recently used via `move_to_end`.\n4. If cache miss, compute result, insert, and evict head if `len > capacity`.",
    "explanation": "`OrderedDict` maintains double-linked list ordering behind hash table lookups, granting O(1) retrieval and O(1) eviction.",
    "time_complexity": "O(1) per lookup/insertion",
    "space_complexity": "O(Capacity)",
    "id": 20,
    "status": "unattempted"
  },
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
    "starter_code": "public class Student {\n    // Declare private fields, constructor, and displayDetails()\n}\n",
    "solution": "public class Student {\n    private String name;\n    private int rollNumber;\n    private String grade;\n\n    public Student(String name, int rollNumber, String grade) {\n        this.name = name;\n        this.rollNumber = rollNumber;\n        this.grade = grade;\n    }\n\n    public void displayDetails() {\n        System.out.println(\"Name: \" + name + \", Roll: \" + rollNumber + \", Grade: \" + grade);\n    }\n}\n",
    "approach": "1. Define private member variables for data protection.\n2. Provide parameterized constructor using `this.name = name`.\n3. Implement public display method for formatted output.",
    "explanation": "Encapsulation restricts direct variable access and bundles data with the methods that operate on it, a core tenet of Object-Oriented Programming.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 21,
    "status": "unattempted"
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
    "starter_code": "public class MinMaxFinder {\n    public static void findMinMax(int[] nums) {\n        // Print Min and Max\n    }\n}\n",
    "solution": "public class MinMaxFinder {\n    public static void findMinMax(int[] nums) {\n        if (nums == null || nums.length == 0) return;\n        int min = nums[0];\n        int max = nums[0];\n\n        for (int i = 1; i < nums.length; i++) {\n            if (nums[i] < min) min = nums[i];\n            if (nums[i] > max) max = nums[i];\n        }\n        System.out.println(\"Min: \" + min + \", Max: \" + max);\n    }\n}\n",
    "approach": "1. Guard against empty arrays.\n2. Seed `min = nums[0]` and `max = nums[0]`.\n3. Loop across array updating `min` and `max`.\n4. Print results.",
    "explanation": "A single linear scan determines both boundaries in O(N) operations without sorting.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 22,
    "status": "unattempted"
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
    "starter_code": "public class PalindromeChecker {\n    public static boolean isPalindrome(String str) {\n        // Write your solution here\n        return false;\n    }\n}\n",
    "solution": "public class PalindromeChecker {\n    public static boolean isPalindrome(String str) {\n        if (str == null) return false;\n        int left = 0;\n        int right = str.length() - 1;\n\n        while (left < right) {\n            char cLeft = Character.toLowerCase(str.charAt(left));\n            char cRight = Character.toLowerCase(str.charAt(right));\n            if (cLeft != cRight) {\n                return false;\n            }\n            left++;\n            right--;\n        }\n        return true;\n    }\n}\n",
    "approach": "1. Initialize two pointers: `left = 0`, `right = str.length() - 1`.\n2. Compare characters after `Character.toLowerCase()`.\n3. If mismatch, return false.\n4. Increment `left`, decrement `right` until crossed.\n5. Return true.",
    "explanation": "Two-pointer comparison operates in-place without creating reversed string objects, saving heap allocation.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 23,
    "status": "unattempted"
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
    "starter_code": "public class Rectangle {\n    private double width;\n    private double height;\n\n    // Implement overloaded constructors and getArea()\n}\n",
    "solution": "public class Rectangle {\n    private double width;\n    private double height;\n\n    // Default constructor\n    public Rectangle() {\n        this(1.0, 1.0);\n    }\n\n    // Square constructor\n    public Rectangle(double side) {\n        this(side, side);\n    }\n\n    // Full constructor\n    public Rectangle(double width, double height) {\n        this.width = width;\n        this.height = height;\n    }\n\n    public double getArea() {\n        return this.width * this.height;\n    }\n}\n",
    "approach": "1. Create full constructor setting width and height.\n2. Overload single-parameter constructor calling `this(side, side)`.\n3. Overload default constructor calling `this(1.0, 1.0)`.\n4. Implement `getArea()`.",
    "explanation": "Constructor overloading allows flexible object instantiation. Chaining through `this()` avoids duplicating initialization logic.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 24,
    "status": "unattempted"
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
    "starter_code": "public class Calculator {\n    // Implement overloaded add methods\n}\n",
    "solution": "public class Calculator {\n    public int add(int a, int b) {\n        return a + b;\n    }\n\n    public int add(int a, int b, int c) {\n        return a + b + c;\n    }\n\n    public double add(double a, double b) {\n        return a + b;\n    }\n}\n",
    "approach": "1. Define `add(int, int)`.\n2. Overload with `add(int, int, int)`.\n3. Overload with `add(double, double)`.",
    "explanation": "Compile-time polymorphism resolves the target method based on the compile-time type and count of arguments.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 25,
    "status": "unattempted"
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
    "starter_code": "public class Employee {\n    protected double baseSalary;\n    // Implement constructor and calculateSalary()\n}\n\nclass Manager extends Employee {\n    private double bonus;\n    // Implement constructor and override calculateSalary()\n}\n",
    "solution": "public class Employee {\n    protected double baseSalary;\n\n    public Employee(double baseSalary) {\n        this.baseSalary = baseSalary;\n    }\n\n    public double calculateSalary() {\n        return this.baseSalary;\n    }\n}\n\nclass Manager extends Employee {\n    private double bonus;\n\n    public Manager(double baseSalary, double bonus) {\n        super(baseSalary);\n        this.bonus = bonus;\n    }\n\n    @Override\n    public double calculateSalary() {\n        return super.calculateSalary() + this.bonus;\n    }\n}\n",
    "approach": "1. Base class `Employee` provides constructor and `calculateSalary()`.\n2. Derived class `Manager` calls `super(baseSalary)`.\n3. Override `calculateSalary()` adding `bonus`.",
    "explanation": "Method overriding provides runtime polymorphism. `super` invokes the immediate parent's implementation.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 26,
    "status": "unattempted"
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
    "starter_code": "interface Playable {\n    void play();\n}\n\n// Implement Guitar and Piano\n",
    "solution": "interface Playable {\n    void play();\n}\n\nclass Guitar implements Playable {\n    @Override\n    public void play() {\n        System.out.println(\"Strumming Guitar chords\");\n    }\n}\n\nclass Piano implements Playable {\n    @Override\n    public void play() {\n        System.out.println(\"Playing Piano keys\");\n    }\n}\n",
    "approach": "1. Declare `Playable` interface.\n2. Implement `Guitar` with specific `play()` printout.\n3. Implement `Piano` with specific `play()` printout.",
    "explanation": "Interfaces establish a contract for what a class must do without dictating how, enabling decoupled modular architecture.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 27,
    "status": "unattempted"
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
    "starter_code": "// Define InvalidAgeException and Validator class\n",
    "solution": "class InvalidAgeException extends Exception {\n    public InvalidAgeException(String message) {\n        super(message);\n    }\n}\n\npublic class AgeValidator {\n    public static void validateAge(int age) throws InvalidAgeException {\n        if (age < 18) {\n            throw new InvalidAgeException(\"Age must be 18 or older to register\");\n        }\n        System.out.println(\"Registration eligible\");\n    }\n}\n",
    "approach": "1. Create class extending `Exception` with message constructor.\n2. In `validateAge`, check condition `age < 18`.\n3. Throw new exception instance if invalid.\n4. Mark method signature with `throws InvalidAgeException`.",
    "explanation": "Custom exceptions clarify application-specific domain errors and force callers to handle failure scenarios gracefully.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 28,
    "status": "unattempted"
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
    "starter_code": "public class Pair<K, V> {\n    // Implement generic Pair\n}\n",
    "solution": "public class Pair<K, V> {\n    private K key;\n    private V value;\n\n    public Pair(K key, V value) {\n        this.key = key;\n        this.value = value;\n    }\n\n    public K getKey() { return key; }\n    public void setKey(K key) { this.key = key; }\n\n    public V getValue() { return value; }\n    public void setValue(V value) { this.value = value; }\n\n    @Override\n    public String toString() {\n        return \"(\" + key + \", \" + value + \")\";\n    }\n}\n",
    "approach": "1. Declare class with type parameters `<K, V>`.\n2. Store private members `key` and `value`.\n3. Provide getters and setters.\n4. Override `toString()`.",
    "explanation": "Java generics provide compile-time type safety, eliminating type casts and preventing `ClassCastException` at runtime.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 29,
    "status": "unattempted"
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
    "starter_code": "public class BoundedBuffer {\n    private int data;\n    private boolean hasData = false;\n\n    public synchronized void produce(int value) throws InterruptedException {\n        // Implement produce\n    }\n\n    public synchronized int consume() throws InterruptedException {\n        // Implement consume\n        return 0;\n    }\n}\n",
    "solution": "public class BoundedBuffer {\n    private int data;\n    private boolean hasData = false;\n\n    public synchronized void produce(int value) throws InterruptedException {\n        while (hasData) {\n            wait();\n        }\n        this.data = value;\n        this.hasData = true;\n        notifyAll();\n    }\n\n    public synchronized int consume() throws InterruptedException {\n        while (!hasData) {\n            wait();\n        }\n        int result = this.data;\n        this.hasData = false;\n        notifyAll();\n        return result;\n    }\n}\n",
    "approach": "1. Keep state flag `hasData`.\n2. In `produce`, wait while buffer is full; write data, set flag, notify.\n3. In `consume`, wait while empty; read data, reset flag, notify.\n4. Protect methods with `synchronized` monitor lock.",
    "explanation": "Guarded blocks using `wait()` release the intrinsic monitor lock and suspend execution until signaled, coordinating concurrent threads without busy waiting.",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "id": 30,
    "status": "unattempted"
  },
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
    "starter_code": "def insert_at_index(arr: list, n: int, idx: int, val: int) -> list:\n    # Shift elements right and insert\n    pass\n",
    "solution": "def insert_at_index(arr: list, n: int, idx: int, val: int) -> list:\n    arr.append(None)\n    for i in range(n, idx, -1):\n        arr[i] = arr[i - 1]\n    arr[idx] = val\n    return arr\n",
    "approach": "1. Expand list by one slot.\n2. Shift elements right from index `n` down to `idx + 1`.\n3. Place `val` at index `idx`.\n4. Return array.",
    "explanation": "Inserting into a contiguous array requires shifting all subsequent elements to maintain contiguous ordering.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 31,
    "status": "unattempted"
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
    "starter_code": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef traverse_list(head: ListNode) -> list:\n    # Collect values\n    pass\n",
    "solution": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef traverse_list(head: ListNode) -> list:\n    values = []\n    curr = head\n    while curr:\n        values.append(curr.val)\n        curr = curr.next\n    return values\n",
    "approach": "1. Set current pointer to `head`.\n2. While current is not null, record `curr.val`.\n3. Advance `curr = curr.next`.\n4. Return collected list.",
    "explanation": "Unlike arrays, linked lists are stored non-contiguously in memory; traversal requires following pointer links one node at a time.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1) auxiliary",
    "id": 32,
    "status": "unattempted"
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
    "starter_code": "class ArrayStack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, val): pass\n    def pop(self): pass\n    def peek(self): pass\n    def is_empty(self) -> bool: pass\n    def size(self) -> int: pass\n",
    "solution": "class ArrayStack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, val):\n        self._items.append(val)\n\n    def pop(self):\n        if self.is_empty():\n            raise IndexError(\"pop from empty stack\")\n        return self._items.pop()\n\n    def peek(self):\n        if self.is_empty():\n            raise IndexError(\"peek from empty stack\")\n        return self._items[-1]\n\n    def is_empty(self) -> bool:\n        return len(self._items) == 0\n\n    def size(self) -> int:\n        return len(self._items)\n",
    "approach": "1. Maintain internal list.\n2. `push` appends to tail.\n3. `pop` removes and returns tail.\n4. `peek` inspects index -1.",
    "explanation": "Operating at the end of a dynamic array guarantees amortized O(1) performance for all core stack operations.",
    "time_complexity": "O(1) amortized for all operations",
    "space_complexity": "O(N)",
    "id": 33,
    "status": "unattempted"
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
    "starter_code": "class MyCircularQueue:\n    def __init__(self, k: int):\n        # Initialize circular queue\n        pass\n",
    "solution": "class MyCircularQueue:\n    def __init__(self, k: int):\n        self.capacity = k\n        self.queue = [0] * k\n        self.head = 0\n        self.tail = -1\n        self.size = 0\n\n    def enqueue(self, value: int) -> bool:\n        if self.is_full():\n            return False\n        self.tail = (self.tail + 1) % self.capacity\n        self.queue[self.tail] = value\n        self.size += 1\n        return True\n\n    def dequeue(self) -> bool:\n        if self.is_empty():\n            return False\n        self.head = (self.head + 1) % self.capacity\n        self.size -= 1\n        return True\n\n    def front(self) -> int:\n        return -1 if self.is_empty() else self.queue[self.head]\n\n    def is_empty(self) -> bool:\n        return self.size == 0\n\n    def is_full(self) -> bool:\n        return self.size == self.capacity\n",
    "approach": "1. Track `head`, `tail`, and `size`.\n2. On enqueue, advance `tail = (tail + 1) % capacity`.\n3. On dequeue, advance `head = (head + 1) % capacity`.\n4. Modulo arithmetic wraps indices continuously.",
    "explanation": "A circular queue reuses vacated array slots at the front of the buffer without shifting remaining elements.",
    "time_complexity": "O(1) for all operations",
    "space_complexity": "O(K)",
    "id": 34,
    "status": "unattempted"
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
    "starter_code": "def find_middle_node(head):\n    # Two-pointer tortoise and hare\n    pass\n",
    "solution": "def find_middle_node(head):\n    slow = head\n    fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow\n",
    "approach": "1. Initialize `slow = head` and `fast = head`.\n2. In loop, advance `slow` by 1 node and `fast` by 2 nodes.\n3. When `fast` reaches end or null, `slow` is exactly at the midpoint.\n4. Return `slow`.",
    "explanation": "Because `fast` travels at twice the speed of `slow`, when `fast` finishes traversing the list, `slow` must be at the halfway mark in a single pass.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 35,
    "status": "unattempted"
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
    "starter_code": "def reverse_linked_list(head):\n    # Iterative pointer reversal\n    pass\n",
    "solution": "def reverse_linked_list(head):\n    prev = None\n    curr = head\n    while curr:\n        next_node = curr.next\n        curr.next = prev\n        prev = curr\n        curr = next_node\n    return prev\n",
    "approach": "1. Start with `prev = None` and `curr = head`.\n2. Save `next_node = curr.next`.\n3. Reverse direction: `curr.next = prev`.\n4. Advance `prev = curr` and `curr = next_node`.\n5. When loop terminates, `prev` is the new head.",
    "explanation": "Modifying next pointers in-place reverses the entire list in O(N) operations using zero extra heap memory.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 36,
    "status": "unattempted"
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
    "starter_code": "def is_valid_parentheses(s: str) -> bool:\n    # Use stack\n    pass\n",
    "solution": "def is_valid_parentheses(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n\n    return len(stack) == 0\n",
    "approach": "1. Create mapping of closing brackets to opening brackets.\n2. Iterate through characters.\n3. If closing bracket, pop from stack and check match.\n4. If opening bracket, push to stack.\n5. Return True if stack is completely empty.",
    "explanation": "A LIFO stack matches the most recently opened bracket with the first encountered closing bracket.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 37,
    "status": "unattempted"
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
    "starter_code": "class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef insert_bst(root, val): pass\ndef inorder_traversal(root): pass\n",
    "solution": "class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\ndef insert_bst(root, val):\n    if not root:\n        return TreeNode(val)\n    if val < root.val:\n        root.left = insert_bst(root.left, val)\n    else:\n        root.right = insert_bst(root.right, val)\n    return root\n\ndef inorder_traversal(root):\n    res = []\n    def _inorder(node):\n        if not node: return\n        _inorder(node.left)\n        res.append(node.val)\n        _inorder(node.right)\n    _inorder(root)\n    return res\n",
    "approach": "1. In `insert_bst`, compare `val` to current node to decide left or right branch.\n2. In `inorder_traversal`, visit Left subtree, append Root value, visit Right subtree.",
    "explanation": "Inorder traversal of any valid BST naturally produces elements in non-decreasing sorted order.",
    "time_complexity": "O(H) insertion where H is height, O(N) traversal",
    "space_complexity": "O(H) recursion stack",
    "id": 38,
    "status": "unattempted"
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
    "starter_code": "def has_cycle(head) -> bool:\n    # Floyd's cycle-finding algorithm\n    pass\n",
    "solution": "def has_cycle(head) -> bool:\n    if not head or not head.next:\n        return False\n    slow = head\n    fast = head.next\n    while slow != fast:\n        if not fast or not fast.next:\n            return False\n        slow = slow.next\n        fast = fast.next.next\n    return True\n",
    "approach": "1. Initialize `slow = head` and `fast = head.next`.\n2. In while loop, check if `slow == fast` (collision).\n3. Advance `slow` by 1 and `fast` by 2.\n4. If `fast` hits `None`, no cycle exists.",
    "explanation": "In a closed loop of length C, the relative distance between the two pointers decreases by 1 step in each iteration, guaranteeing collision within O(N) steps.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 39,
    "status": "unattempted"
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
    "starter_code": "from collections import deque\n\ndef level_order(root) -> list[list[int]]:\n    # Breadth-first search queue\n    pass\n",
    "solution": "from collections import deque\n\ndef level_order(root) -> list[list[int]]:\n    if not root:\n        return []\n    result = []\n    queue = deque([root])\n\n    while queue:\n        level_size = len(queue)\n        current_level = []\n        for _ in range(level_size):\n            node = queue.popleft()\n            current_level.append(node.val)\n            if node.left:\n                queue.append(node.left)\n            if node.right:\n                queue.append(node.right)\n        result.append(current_level)\n\n    return result\n",
    "approach": "1. Initialize queue with `root`.\n2. In while loop, capture `level_size = len(queue)`.\n3. Dequeue `level_size` nodes, collecting their values and enqueueing their children.\n4. Append level list to result.",
    "explanation": "Breadth-First Search processes all neighbors at distance d before moving to distance d+1, yielding clean hierarchical level partitions.",
    "time_complexity": "O(N)",
    "space_complexity": "O(W) where W is maximum width of tree",
    "id": 40,
    "status": "unattempted"
  },
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
    "starter_code": "def linear_search(arr: list[int], target: int) -> int:\n    # Sequential scan\n    pass\n",
    "solution": "def linear_search(arr: list[int], target: int) -> int:\n    for idx, val in enumerate(arr):\n        if val == target:\n            return idx\n    return -1\n",
    "approach": "1. Loop through array inspecting each element.\n2. If current element matches `target`, return its index.\n3. If loop finishes without match, return -1.",
    "explanation": "Linear search is the simplest search algorithm, requiring no sorting or prior assumptions about data ordering.",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "id": 41,
    "status": "unattempted"
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
    "starter_code": "def binary_search(nums: list[int], target: int) -> int:\n    # Logarithmic search\n    pass\n",
    "solution": "def binary_search(nums: list[int], target: int) -> int:\n    low = 0\n    high = len(nums) - 1\n\n    while low <= high:\n        mid = low + (high - low) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n\n    return -1\n",
    "approach": "1. Set pointers `low = 0` and `high = len - 1`.\n2. While `low <= high`, calculate `mid`.\n3. Compare `nums[mid]` to `target`.\n4. Halve the search space based on comparison.",
    "explanation": "Halving the search space in each iteration yields O(log N) efficiency, searching 1 billion items in at most 30 comparisons.",
    "time_complexity": "O(log N)",
    "space_complexity": "O(1)",
    "id": 42,
    "status": "unattempted"
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
    "starter_code": "def bubble_sort(arr: list[int]) -> list[int]:\n    # Optimized bubble sort\n    pass\n",
    "solution": "def bubble_sort(arr: list[int]) -> list[int]:\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break\n    return arr\n",
    "approach": "1. Iterate `i` from 0 to n-1.\n2. In inner loop, compare adjacent elements `arr[j]` and `arr[j+1]`.\n3. Swap if out of order and set `swapped = True`.\n4. If `not swapped`, terminate early.",
    "explanation": "With the `swapped` flag, Bubble Sort detects already-sorted inputs in best-case O(N) time.",
    "time_complexity": "O(N^2) average/worst, O(N) best case",
    "space_complexity": "O(1)",
    "id": 43,
    "status": "unattempted"
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
    "starter_code": "def my_pow(x: float, n: int) -> float:\n    # Binary exponentiation\n    pass\n",
    "solution": "def my_pow(x: float, n: int) -> float:\n    if n == 0:\n        return 1.0\n    if n < 0:\n        return 1.0 / my_pow(x, -n)\n\n    half = my_pow(x, n // 2)\n    if n % 2 == 0:\n        return half * half\n    else:\n        return half * half * x\n",
    "approach": "1. Base case: `n == 0` returns 1.0.\n2. If `n < 0`, return `1.0 / my_pow(x, -n)`.\n3. Recursively compute `half = my_pow(x, n // 2)`.\n4. If even, return `half * half`; if odd, multiply by `x`.",
    "explanation": "Binary exponentiation reduces multiplication steps from O(N) to O(log N) by squaring intermediate powers.",
    "time_complexity": "O(log N)",
    "space_complexity": "O(log N) stack depth",
    "id": 44,
    "status": "unattempted"
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
    "starter_code": "def merge_sort(arr: list[int]) -> list[int]:\n    # Divide and conquer\n    pass\n",
    "solution": "def merge_sort(arr: list[int]) -> list[int]:\n    if len(arr) <= 1:\n        return arr\n\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n\n    # Merge step\n    merged = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            merged.append(left[i])\n            i += 1\n        else:\n            merged.append(right[j])\n            j += 1\n    merged.extend(left[i:])\n    merged.extend(right[j:])\n    return merged\n",
    "approach": "1. Base case: array with length <= 1 is already sorted.\n2. Divide: split into `left` and `right` sub-arrays.\n3. Conquer: recursively sort each half.\n4. Combine: merge two sorted arrays using two pointers.",
    "explanation": "Merge sort guarantees stable O(N log N) sorting across worst, average, and best cases.",
    "time_complexity": "O(N log N)",
    "space_complexity": "O(N)",
    "id": 45,
    "status": "unattempted"
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
    "starter_code": "def quick_sort(arr: list[int], low: int, high: int):\n    # In-place partition quick sort\n    pass\n",
    "solution": "def partition(arr, low, high):\n    pivot = arr[high]\n    i = low - 1\n    for j in range(low, high):\n        if arr[j] <= pivot:\n            i += 1\n            arr[i], arr[j] = arr[j], arr[i]\n    arr[i + 1], arr[high] = arr[high], arr[i + 1]\n    return i + 1\n\ndef quick_sort(arr: list[int], low: int = 0, high: int = None):\n    if high is None:\n        high = len(arr) - 1\n    if low < high:\n        pi = partition(arr, low, high)\n        quick_sort(arr, low, pi - 1)\n        quick_sort(arr, pi + 1, high)\n    return arr\n",
    "approach": "1. Select pivot (e.g. `arr[high]`).\n2. Partition elements so items <= pivot are on left.\n3. Place pivot at boundary index `i + 1`.\n4. Recursively sort left and right sub-arrays.",
    "explanation": "Quick Sort is typically the fastest general-purpose in-memory sorting algorithm in practice due to excellent cache locality.",
    "time_complexity": "O(N log N) average, O(N^2) worst case",
    "space_complexity": "O(log N) stack space",
    "id": 46,
    "status": "unattempted"
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
    "starter_code": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Hash map complement lookup\n    pass\n",
    "solution": "def two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for idx, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], idx]\n        seen[num] = idx\n    return []\n",
    "approach": "1. Initialize hash map `seen`.\n2. Iterate through `nums` with indices.\n3. Compute `complement = target - num`.\n4. If complement in `seen`, return `[seen[complement], idx]`.\n5. Otherwise record `seen[num] = idx`.",
    "explanation": "Hashing reduces the brute-force O(N^2) search down to a single O(N) pass by transforming searching into constant-time key lookup.",
    "time_complexity": "O(N)",
    "space_complexity": "O(N)",
    "id": 47,
    "status": "unattempted"
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
    "starter_code": "from collections import deque\n\ndef bfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:\n    # Queue-based traversal\n    pass\n",
    "solution": "from collections import deque\n\ndef bfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:\n    visited = set([start])\n    queue = deque([start])\n    traversal = []\n\n    while queue:\n        vertex = queue.popleft()\n        traversal.append(vertex)\n        for neighbor in graph.get(vertex, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n\n    return traversal\n",
    "approach": "1. Enqueue `start` and add to `visited` set.\n2. While queue is not empty, pop head `vertex` and record.\n3. For each unvisited neighbor, mark visited and enqueue.\n4. Return traversal order.",
    "explanation": "BFS explores graph nodes in order of shortest distance from the source, making it ideal for shortest-path finding on unweighted graphs.",
    "time_complexity": "O(V + E)",
    "space_complexity": "O(V)",
    "id": 48,
    "status": "unattempted"
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
    "starter_code": "def dfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:\n    # Recursive DFS\n    pass\n",
    "solution": "def dfs_graph(graph: dict[int, list[int]], start: int) -> list[int]:\n    visited = set()\n    order = []\n\n    def _dfs(node):\n        visited.add(node)\n        order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                _dfs(neighbor)\n\n    _dfs(start)\n    return order\n",
    "approach": "1. Maintain `visited` set and `order` list.\n2. In helper `_dfs(node)`, add to visited and order.\n3. Iterate neighbors; if not visited, recurse immediately.\n4. Backtrack naturally as calls return.",
    "explanation": "DFS explores deep into paths before backtracking, fundamental for topological sorting, cycle detection, and strongly connected components.",
    "time_complexity": "O(V + E)",
    "space_complexity": "O(V) call stack",
    "id": 49,
    "status": "unattempted"
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
    "starter_code": "def knapsack(values: list[int], weights: list[int], W: int) -> int:\n    # 0/1 Knapsack Dynamic Programming\n    pass\n",
    "solution": "def knapsack(values: list[int], weights: list[int], W: int) -> int:\n    n = len(values)\n    dp = [[0] * (W + 1) for _ in range(n + 1)]\n\n    for i in range(1, n + 1):\n        for w in range(W + 1):\n            if weights[i - 1] <= w:\n                dp[i][w] = max(\n                    dp[i - 1][w],\n                    dp[i - 1][w - weights[i - 1]] + values[i - 1]\n                )\n            else:\n                dp[i][w] = dp[i - 1][w]\n\n    return dp[n][W]\n",
    "approach": "1. Initialize 2D table `dp[n+1][W+1]` with 0s.\n2. Outer loop `i` over items, inner loop `w` over capacities.\n3. If item fits, choose `max(exclude item, include item + value)`.\n4. If item exceeds `w`, exclude it.\n5. Answer is in `dp[n][W]`.",
    "explanation": "Dynamic programming avoids overlapping subproblem re-computations by caching intermediate optimal solutions in a table.",
    "time_complexity": "O(N * W)",
    "space_complexity": "O(N * W)",
    "id": 50,
    "status": "unattempted"
  }
];

export const MOCK_PRACTICE_STATS = {
  "total_questions": 50,
  "completed_questions": 0,
  "completion_percentage": 0,
  "by_category": {
    "C Programming": {
      "total": 10,
      "completed": 0
    },
    "Python": {
      "total": 10,
      "completed": 0
    },
    "Java": {
      "total": 10,
      "completed": 0
    },
    "Data Structures": {
      "total": 10,
      "completed": 0
    },
    "DSA": {
      "total": 10,
      "completed": 0
    }
  },
  "by_difficulty": {
    "Beginner": {
      "total": 19,
      "completed": 0
    },
    "Intermediate": {
      "total": 20,
      "completed": 0
    },
    "Advanced": {
      "total": 11,
      "completed": 0
    }
  }
};

export const MOCK_PROFILE = {
  "id": 1,
  "user_id": 1,
  "full_name": "Arif Mohamed",
  "education": "B.Tech",
  "branch": "Artificial Intelligence and Data Science",
  "year": 3,
  "institution": "Anna University Affiliated Engineering College",
  "interests": [
    "Machine Learning",
    "Computer Vision",
    "Deep Learning",
    "Python"
  ],
  "strengths": [
    "Analytical Thinking",
    "Problem Solving",
    "Python Programming"
  ],
  "certifications": [
    "Python for Data Science",
    "Machine Learning Specialization"
  ],
  "projects": [
    {
      "title": "Student Performance Predictor",
      "description": "Regression model predicting exam scores from study habits."
    },
    {
      "title": "Road Sign Classifier",
      "description": "Convolutional neural network for traffic sign recognition."
    }
  ],
  "career_goal": "AI/ML Engineer",
  "goal_status": "known",
  "weekly_hours": 15,
  "language": "en",
  "learner_pace_factor": 1.0,
  "cohort_id": 1
};

export const MOCK_MATCH = {
  "overall_score": 74,
  "career_name": "AI/ML Engineer",
  "target_role": "AI/ML Engineer",
  "breakdown": {
    "core_skills": 78,
    "practical_projects": 72,
    "domain_knowledge": 80,
    "portfolio_readiness": 66
  },
  "missing_skills": [
    "PyTorch Deep Learning",
    "MLOps & Model Deployment",
    "Docker for ML",
    "FastAPI Microservices"
  ],
  "matched_skills": [
    "Python Programming",
    "NumPy & Pandas",
    "Data Analysis",
    "Scikit-Learn",
    "SQL Queries"
  ],
  "insights": "You have strong fundamentals in Python and tabular data modeling. Focus next on deep neural networks and containerized deployment to reach job readiness."
};

export const MOCK_ROADMAP = {
  "career_name": "AI/ML Engineer",
  "total_stages": 4,
  "current_stage": 2,
  "stages": [
    {
      "id": 1,
      "title": "Stage 1: Core Mathematical & Python Foundations",
      "status": "completed",
      "duration_weeks": 4,
      "items": [
        {
          "id": 101,
          "title": "Linear Algebra & Matrix Operations",
          "status": "completed",
          "type": "concept"
        },
        {
          "id": 102,
          "title": "Data Manipulation with Pandas & NumPy",
          "status": "completed",
          "type": "practice"
        },
        {
          "id": 103,
          "title": "Exploratory Data Analysis Mini-Project",
          "status": "completed",
          "type": "project"
        }
      ]
    },
    {
      "id": 2,
      "title": "Stage 2: Supervised & Unsupervised Machine Learning",
      "status": "in_progress",
      "duration_weeks": 6,
      "items": [
        {
          "id": 201,
          "title": "Scikit-Learn Pipelines & Feature Engineering",
          "status": "completed",
          "type": "concept"
        },
        {
          "id": 202,
          "title": "Classification & Regression Benchmarks",
          "status": "in_progress",
          "type": "practice"
        },
        {
          "id": 203,
          "title": "Model Evaluation & Hyperparameter Tuning",
          "status": "pending",
          "type": "practice"
        }
      ]
    },
    {
      "id": 3,
      "title": "Stage 3: Deep Learning & Computer Vision",
      "status": "pending",
      "duration_weeks": 6,
      "items": [
        {
          "id": 301,
          "title": "PyTorch Tensors and Neural Network Architecture",
          "status": "pending",
          "type": "concept"
        },
        {
          "id": 302,
          "title": "Convolutional Networks for Image Classification",
          "status": "pending",
          "type": "project"
        },
        {
          "id": 303,
          "title": "Transfer Learning with Pre-trained Models",
          "status": "pending",
          "type": "practice"
        }
      ]
    },
    {
      "id": 4,
      "title": "Stage 4: MLOps, API Packaging & Capstone",
      "status": "pending",
      "duration_weeks": 4,
      "items": [
        {
          "id": 401,
          "title": "FastAPI Inference Service with Docker Container",
          "status": "pending",
          "type": "project"
        },
        {
          "id": 402,
          "title": "End-to-End Capstone Project on Cloud",
          "status": "pending",
          "type": "capstone"
        }
      ]
    }
  ]
};

export const MOCK_CAREERS = [
  {
    "id": 1,
    "slug": "ai-ml-engineer",
    "name": "AI/ML Engineer",
    "match_pct": 74,
    "plain_reason": "Matches your Python background and strong interest in machine learning algorithms.",
    "suits_who": "Learners who enjoy mathematics, coding, and teaching computers to solve complex problems.",
    "demand_level": "High",
    "entry_titles": [
      "Junior ML Engineer",
      "Associate Data Scientist",
      "AI Developer"
    ]
  },
  {
    "id": 2,
    "slug": "full-stack-developer",
    "name": "Full Stack Developer",
    "match_pct": 68,
    "plain_reason": "Builds complete end-to-end web apps combining user interfaces with databases.",
    "suits_who": "Learners who want to create tangible products and master both client and server code.",
    "demand_level": "Very High",
    "entry_titles": [
      "Junior Full Stack Developer",
      "Software Engineer",
      "Frontend/Backend Engineer"
    ]
  },
  {
    "id": 3,
    "slug": "data-analyst",
    "name": "Data Analyst",
    "match_pct": 82,
    "plain_reason": "Leverages your SQL, Pandas, and statistics strengths to uncover business insights.",
    "suits_who": "Learners who like analyzing trends, building dashboards, and answering business questions.",
    "demand_level": "High",
    "entry_titles": [
      "Junior Data Analyst",
      "BI Analyst",
      "Analytics Associate"
    ]
  },
  {
    "id": 4,
    "slug": "cloud-devops-engineer",
    "name": "Cloud & DevOps Engineer",
    "match_pct": 60,
    "plain_reason": "Automates deployment, manages cloud infrastructure, and guarantees system reliability.",
    "suits_who": "Learners interested in Linux, networks, Docker, CI/CD, and scalable cloud systems.",
    "demand_level": "Very High",
    "entry_titles": [
      "Cloud Associate",
      "DevOps Engineer",
      "Site Reliability Engineer"
    ]
  }
];

export const MOCK_AGENT_LOGS = [
  {
    "id": 1,
    "agent": "Orchestrator",
    "action": "Assessed profile and synthesized learning roadmap",
    "timestamp": "Just now",
    "status": "success"
  },
  {
    "id": 2,
    "agent": "Gap Analyzer",
    "action": "Evaluated skill inventory against AI/ML Engineer profile",
    "timestamp": "10m ago",
    "status": "success"
  },
  {
    "id": 3,
    "agent": "Learning Coach",
    "action": "Scheduled Sprint 3 exercises and practice questions",
    "timestamp": "25m ago",
    "status": "success"
  },
  {
    "id": 4,
    "agent": "Roadmap Generator",
    "action": "Calculated milestone target dates based on 15h/week pacing",
    "timestamp": "1h ago",
    "status": "success"
  }
];

export const MOCK_PROGRESS = {
  "overall_progress": 42,
  "hours_spent": 48,
  "target_hours": 120,
  "streak_days": 5,
  "completed_milestones": 8,
  "total_milestones": 19,
  "weekly_trend": [
    8,
    12,
    14,
    15,
    12,
    16,
    15
  ]
};

export const MOCK_FIRST_WEEK = {
  "title": "Your First Week Action Plan",
  "summary": "Kickstart your AI/ML journey with targeted daily tasks",
  "days": [
    {
      "day": 1,
      "task": "Set up PyTorch and verify GPU acceleration in Python environment",
      "completed": true,
      "duration": "1.5 hrs"
    },
    {
      "day": 2,
      "task": "Solve 3 beginner practice questions on Python lists and dictionaries",
      "completed": true,
      "duration": "1.5 hrs"
    },
    {
      "day": 3,
      "task": "Review gradient descent and backpropagation principles",
      "completed": false,
      "duration": "2 hrs"
    },
    {
      "day": 4,
      "task": "Implement a simple binary logistic regression classifier from scratch",
      "completed": false,
      "duration": "2 hrs"
    },
    {
      "day": 5,
      "task": "Complete Sprint 2 knowledge checkpoint assessment",
      "completed": false,
      "duration": "1 hr"
    }
  ]
};

export const MOCK_CURRENT_SPRINT = {
  "id": 2,
  "title": "Sprint 2: Classification Pipelines & Practice Challenges",
  "start_date": "2026-11-10",
  "end_date": "2026-11-24",
  "status": "in_progress",
  "progress_pct": 50,
  "tasks": [
    {
      "id": 1,
      "title": "Complete C and Python practice modules",
      "completed": true
    },
    {
      "id": 2,
      "title": "Train Random Forest baseline on tabular benchmark",
      "completed": true
    },
    {
      "id": 3,
      "title": "Build confusion matrix and ROC curve visualizations",
      "completed": false
    },
    {
      "id": 4,
      "title": "Package notebook into modular Python script",
      "completed": false
    }
  ]
};
