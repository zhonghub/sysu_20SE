#include<iostream>
#include<string>
using namespace std;
int myhash1(const string s,int n){//BKDRHash算法
    int hash = 0 ;
    int i = 0 ;
    while(s[i]){
    	hash =(hash*131) + (int)(s[i++]);     
    }
    return (hash & 0x7FFFFFFF)%n;
}

int myhash2(const string str,int n){//DJBHash算法
    int hash = 5381;
    int i = 0;
    while(str[i])
    hash += (hash << 5) + (str[i++]);
    return (hash & 0x7FFFFFFF)%n;
    }

int myhash3(const string str,int n){//JSHash算法
    int hash = 1315423911;
    int i = 0;
    while(str[i])
    hash ^= ((hash << 5) + (str[i++]) + (hash >> 2));;
    return (hash & 0x7FFFFFFF)%n;
    }
    
int myhash4(const string str,int n){//RSHash算法
    unsigned int b = 378551;
    unsigned int a = 63689;
    unsigned int hash = 0;
    int i = 0;
    while (str[i]){
        hash = hash * a + (str[i++]);
        a *= b;
    } 
    return (hash & 0x7FFFFFFF)%n;
}

int myhash5(const string str,int n){//SDBMHash算法
    unsigned int hash = 0;
    int i = 0;
    while (str[i]){
        // equivalent to: hash = 65599*hash + (*str++);
        hash = (str[i++]) + (hash << 6) + (hash << 16) - hash;
    }
    return (hash & 0x7FFFFFFF)%n;
}

int myhash6(const string str,int n){//ELFHash算法
    unsigned int hash = 0;
    unsigned int x    = 0;
    int i = 0 ;
    while (str[i]){
        hash = (hash << 4) + (str[i++]);
        if ((x = hash & 0xF0000000L) != 0){
                hash ^= (x >> 24);
                hash &= ~x;
        }
    }
    return (hash & 0x7FFFFFFF)%n;
}
