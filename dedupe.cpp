//我把相同軌跡的去除(保留R開頭的組合，L開頭的組合去除掉)、全為R或全為L的也去除
//請輸入n
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

int main(){
    int n;
    cin >> n;
    int total = pow(2, n);
    vector<int> v(n, 1);
    for(int i = 1; i<n; i++){
        v[i] = -1;
    }
    while(true){
        bool all_one = true;
        for(int i = 0; i<v.size(); i++){
            if(v[i]!=1){
                all_one = false;
            }
        }
        if(!all_one){
            for(int i = 0; i<v.size(); i++){
                cout << v[i] << " ";
            }
            cout << endl;
        }
        int idx = n-1;
        while(idx>=1){
            if(v[idx]==-1){
                v[idx] = 1;
                break;
            }
            else{
                v[idx] = -1;
                idx--;
            }
        }
        if(idx<1){
            break;
        }
    }
}