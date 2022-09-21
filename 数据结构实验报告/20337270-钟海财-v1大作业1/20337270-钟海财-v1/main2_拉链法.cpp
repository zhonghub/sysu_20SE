#include<iostream>
#include<vector>
#include<string>
using namespace std;
#include <fstream>
#include"myhash.cpp" //包含了使用的hash函数 
int search; //记录不同单词的查找总次数 
int diff_words; //记录不同单词的总数 
int all_words;//记录单词总数 
int hash_k;//选择哈希函数 

struct word{
	string s;
	vector<int> index;//储存单词s存在的句子的序号 
}; 

int myhash(const string s,int n)//字符串的哈希函数，生成最初始的哈希值 
{
	switch(hash_k){ //根据hash_k的值选择使用的哈希函数 
		case 2: return myhash2(s,n);
		case 3: return myhash3(s,n);
		case 4: return myhash4(s,n);
		case 5: return myhash5(s,n);
		case 6: return myhash6(s,n);
		default: return myhash1(s,n);
	}
} 

int getkey(vector<vector<word*> > &table,string s,int n);
//由于使用拉链法解决冲突，返回单词s在哈希表table[myhash(s)][]中的位置 

bool isword(char c);//判断是不是组成单词的数字或字母 
	
void getword(string s,vector<string>& ss); //提取字符串s中的所有单词到vector<string>&ss中 

bool _read(vector<vector<string> >&all,vector<vector<word*> > &table, int n);
 //将text.txt读到vector<vector<string> >&all里,all[k]表示第 k个句子 
//对所有单词遍历并生成对应的table

int main(){
	vector<vector<string> > all;//将所有句子读到 vector<vector<string> >类型的 all里面,all[k]表示第 k个句子 
	cout<<"拉链法:  "<<endl;
	int n = 5000 ;//table的容量 ，由于使用拉链法，可以小于不同单词的个数 
	cout<<"请输入哈希表的容量n:(推荐n>=100) "<<endl ;
	cin>>n; 
	vector<vector<word*> > table;//储存单词所在句子序号，如单词s，key = getkey(table,s,n),
	//所在句子序号储存在table[myhash[s]][key]->index[]里 
	vector<word*> t;
	for(int i = 0 ; i <n; ++i) table.push_back(t); //对table进行初始化赋值  
	hash_k = 1;//默认使用BKDRHash算法的哈希函数myhash1  
	 
	cout<<"哈希函数选择："<<endl
	    <<"1: BKDRHash算法"<<endl
        <<"2: DJBHash算法"<<endl
		<<"3: JSHash算法"<<endl
		<<"4: RSHash算法"<<endl
		<<"5: SDBMHash算法"<<endl
		<<"6: ELFHash算法" <<endl;
	cout<<"请输入整数1~6来选择哈希函数hash_k : "<<endl;
	cin>>hash_k;//选择使用的哈希函数 
	//将所有句子读到 vector<vector<string> >类型的 all里面,all[k]表示第 k个句子 
	bool A1 = _read(all,table,n);//读取text.txt并生成对应的all和table
	ofstream outfile("answer2.txt",ios::out);//输出到文件answer.txt里
	cout<<"all sentences: "<<all.size()<<endl;
	cout<<"all_words: "<<all_words<<endl;
	cout<<"diff_words: "<<diff_words<<endl;
	cout<<"search: "<<search<<endl;
	cout<<"space = n : "<<n<<endl;
	cout<<"n/diff_words: "<<(double)n/(double)diff_words<<endl;
	cout<<"average_search = search/diff_words: "<< (double)search/(double)diff_words <<endl;
	cout<<"-----------------------------------------"<<endl;
	cout<<"You can use '$stop' to stop the Query !"<<endl; 
	cout <<"Query :"<<endl; //测试样例 and 和 amu  在没有解决冲突时hash值相同 
	cout<<"请输入: "; 
	outfile<<"拉链法:  "<<endl; 
	outfile<<"请输入哈希表的容量n:(推荐n>=100) "<<endl<<n<<endl ;
	outfile<<"哈希函数选择："<<endl
	    <<"1: BKDRHash算法"<<endl
        <<"2: DJBHash算法"<<endl
		<<"3: JSHash算法"<<endl
		<<"4: RSHash算法"<<endl
		<<"5: SDBMHash算法"<<endl
		<<"6: ELFHash算法" <<endl;
	outfile<<"请输入整数1~6来选择哈希函数hash_k : "<<endl<<hash_k<<endl;
	outfile<<"all sentences: "<<all.size()<<endl;
	outfile<<"all_words: "<<all_words<<endl;
	outfile<<"diff_words: "<<diff_words<<endl;
	outfile<<"search: "<<search<<endl;
	outfile<<"space = n : "<<n<<endl;
	outfile<<"n/diff_words: "<<(double)n/(double)diff_words<<endl;
	outfile<<"average_search = search/diff_words: "<< (double)search/(double)diff_words <<endl;
	outfile<<"-----------------------------------------"<<endl;
	outfile<<"You can use '$stop' to stop the Query !"<<endl; 
	outfile<<"Query :"<<endl;
	outfile<<"请输入: "; 
	string find; 
	while(cin>>find&&find!="$stop"){//根据输入的单词进行相应操作如查询或退出 
		outfile<<find<<endl; 
	int key1 = myhash(find,n);
	int key2 = getkey(table,find,n);
	if(key2==table[key1].size()){
		cout<<"There is not the word!"<<endl;
		outfile<<"There is not the word!"<<endl;
	}
	else{
		for(int i = 0 ; i <table[key1][key2]->index.size();++i){ 
			cout<<"Sentence "<<table[key1][key2]->index[i]+1 <<endl;
			outfile<<"Sentence "<<table[key1][key2]->index[i]+1 <<endl;
    		for(int j = 0; j <all[table[key1][key2]->index[i]].size() ;++j){
    			cout<<all[table[key1][key2]->index[i]][j]<<" ";
    			outfile<<all[table[key1][key2]->index[i]][j]<<" ";
				}
			cout<<endl; 
			outfile<<endl;
		}	
	}
	cout<<endl<<"-----------------------------------------"<<endl;
	cout<<"You can use '$stop' to stop the Query !"<<endl; 
	cout<< "Query :"<<endl;
	cout<<"请输入: "; 
	outfile<<endl<<"-----------------------------------------"<<endl;
	outfile<<"You can use '$stop' to stop the Query !"<<endl; 
	outfile<< "Query :"<<endl;
	outfile<<"请输入: "; 
	}
	outfile.close();
	return 0;
}

//以下为函数实现 

int getkey(vector<vector<word*> > &table,string ss,int n){//生成单词s在哈希表table[key1]拉链中的索引 
	++all_words;
	int key1 = myhash(ss,n);
    int h= table[key1].size();
    for(int i = 0 ; i < h;++i){ //拉链法 
    	if(table[key1][i]->s == ss) return i;//如果该单词已经在哈希表table[]中时返回该key值 
    }
    search+=(h+1);
    ++diff_words; 
    return h; 
}

bool isword(char c){ //判断是不是组成单词的数字或字母 
	if((int)c>=48 && (int)c <=57) return true;
	else if((int)c>=65 && (int)c <=90) return true;
	else if((int)c>=97 && (int)c <=122) return true;
	else return false;
}
void getword(string s,vector<string>& ss){ //提取字符串s中的所有单词到vector<string>&ss中 
    string word = "";
    int k = 0 ;
    while(k<s.size()){
        word = "";
        while(k<s.size()&& !isword(s[k])){
            ++k;
        }
        while(k<s.size()&& isword(s[k])){
            word.push_back(s[k]);
            ++k;
        }
        if(word!="") ss.push_back(word);
    }
}

bool _read(vector<vector<string> >&all,vector<vector<word*> > &table, int n){ 
//将text.txt读到vector<vector<string> >&all里,all[k]表示第 k个句子 
    ifstream infile("text.txt",ios::in);
    if(!infile.is_open()) return false ;
    int i = 0;
    while(!infile.eof()){
        vector<string> ss;
        string str;
        str.clear();
        infile>>str;
        while(str[str.size()-1]!='\n' &&str[str.size()-1]!='.' &&!infile.eof() && str[str.size()-1]!='!'&&str[str.size()-1]!='?'){ 
		if(str[str.size()-1]=='"' &&(str[str.size()-2]=='.' || str[str.size()-2]=='!'||str[str.size()-2]=='?')) break;
		ss.push_back(str);
    	infile>>str;
    	} 
    	ss.push_back(str);
    	all.push_back(ss); 
    	for(int j = 0; j <all[i].size() ;++j){ //对第i个句子all[i]提取所有单词并存到哈希表里 
    		vector<string> ss;
    		getword(all[i][j],ss);//将字符串 all[i][j]里的所有单词提取到ss里 
    		for(int k = 0; k <ss.size();++k){
    			int key1 = myhash(ss[k],n);
    			int key2 = getkey(table,ss[k],n);//生成单词words[k]的解决冲突之后的哈希值 
    			if(key2==table[key1].size()){
    			word *t0 = new word;
    			t0->s = ss[k] ;
				table[key1].push_back(t0);
				}
				int h = table[key1][key2]->index.size();
      			if(h==0||table[key1][key2]->index[h-1]!=i) //如果该句子未被记录
				  table[key1][key2]->index.push_back(i);//将该句子序号记入对应的table中 
      		}
		}
    	++i;
    } 
    infile.close();
    return true;
}


