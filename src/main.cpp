#include<bits/stdc++.h>
using namespace std;
bool isPalindrome(string temp){
    string reversed_str=temp;
    reverse(reversed_str.begin() , reversed_str.end() );
    return temp == reversed_str;
}
string Solution(string A) {
    int n=A.length();
    string ans;
    int start=0;
    for(int i=0; i<n; i++)
    {
        for(int j=i+1; j<=n; j++)
        {
            string temp=A.substr(i,j-i);
            if(isPalindrome(temp)==1){
                if( temp.length() > ans.length() ){
                    ans=temp;
                    start=i;
                }
                else if(temp.length() == ans.length()){
                    if(i<start){
                        ans=temp;
                        start=i;
                    }
                }
            }
        }
    }
    return ans;
}
int main(){
    string A="aab";
    cout<<Solution(A);
    return 0;
}