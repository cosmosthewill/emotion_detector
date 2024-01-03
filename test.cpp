//----------------------------------------------------------------------------------------\

#include    <iostream>
#include    <cmath>
#include    <iomanip>
#include    <cstdio>
#include    <algorithm>
#include    <string>
#include    <vector>
#include    <stack>
#include    <deque>
#include    <queue>
#include    <map>
#include    <set>
#include    <cstdint>
#define     ll long long
#define     ull unsigned long long
#define     ld long double
#define     prec(k) << fixed << setprecision(k)
#define     up(k, n) for (int i = k ; i < n ; i ++)
#define     down(k, n) for (int i = k ; i >= n ; i --)
#define     maxN 10007
#define     maxM 100007
#define     maxT 1000007
#define     ii pair<int, int>
#define     X first
#define     Y second

//----------------------------------------------------------------------------------------\

using namespace std;
void printPermutation(const vector<int>& permutation) {
    for (int num : permutation) {
        cout << num << " ";
    }
    cout << endl;
}
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int findPermutationIndex(const vector<int>& permutation) {
    int n = permutation.size();
    vector<int> sortedPermutation = permutation;
    sort(sortedPermutation.begin(), sortedPermutation.end());

    int index = 1;
    for (int i = 0; i < n; ++i) {
        auto it = find(sortedPermutation.begin(), sortedPermutation.end(), permutation[i]);
        index += distance(sortedPermutation.begin(), it) * factorial(n - 1 - i);
        sortedPermutation.erase(it);
    }

    return index;
}
int main() {
    int n;
    cin >> n;

    vector<int> sequence(n);
    for (int i = 0; i < n; ++i) {
        sequence[i] = i + 1;
    }
    vector<int> permutation(n);
    for (int i = 0; i < n; ++i) {
        cin >> permutation[i];
    }
    int index1 = findPermutationIndex(permutation);
    cout << index1 << endl;

    // Nhập số thứ tự của hoán vị và in ra hoán vị đó
    int index;
    cin >> index;

    if (index >= 1 && index < factorial(n)) {
        sequence = vector<int>(n);
        for (int i = 0; i < n; ++i) {
            sequence[i] = i + 1;
        }

        for (int i = 1; i < index; ++i) {
            next_permutation(sequence.begin(), sequence.end());
        }
        printPermutation(sequence);
    }

    return 0;
}