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
int getkey(string table[],string s,int n);//生成单词s在哈希表table[]中已经解决冲突的key值 
	//如果该单词已经在哈希表table[]中时返回该key值 

bool isword(char c);//判断是不是组成单词的数字或字母 
	
void getword(string s,vector<string>& ss); //提取字符串s中的所有单词到vector<string>&ss中 

bool _read(vector<vector<string> >&all,vector<vector<int> > &table,string* hash_table, int n);
 //将text.txt读到vector<vector<string> >&all里,all[k]表示第 k个句子 
//对所有单词遍历并生成对应的table和hash_table 

int main(){
	cout<<"开放地址法:  "<<endl; 
	vector<vector<string> > all;//将所有句子读到 vector<vector<string> >类型的 all里面,all[k]表示第 k个句子 
	int n = 4900 ;//hash_table的容量 ，要超过不同单词的个数
	cout<<"请输入哈希表的容量n(推荐n>=4900): "<<endl ;
	cin>>n; 
	string hash_table[n];
	//hash_table为储存单词的哈希表,由getkey(string table[],string s,int n)函数生成对应单词s解决冲突之后的key值
	vector<vector<int> > table;
	//用于储存单词所存在的所有句子的序号，如table[key][]存放了hash值为key的单词所在所有句子的序号 
	vector<int> t;
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
	cin>>hash_k; //输入选择的哈希函数 
	//将所有句子读到 vector<vector<string> >类型的 all里面,all[k]表示第 k个句子 
	bool A1 = _read(all,table,hash_table,n);//读取text.txt文件并生成对应的all，table和hash_table 
	ofstream outfile("answer1.txt",ios::out);//输出到文件answer.txt里 
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
	outfile<<"开放地址法:  "<<endl; 
	outfile<<"请输入哈希表的容量n(推荐n>=4900): "<<endl<<n<<endl ;
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
	string find;//要查询的单词 
	while(cin>>find && find!="$stop"){ //根据输入的单词进行相应操作如查询或退出 
		outfile<<find<<endl; 
		int key = getkey(hash_table,find,n);
		if(table[key].size()==0){//该单词find不存在对应的句子时 
			cout<<"There is not the word!"<<endl;
			outfile<<"There is not the word!"<<endl;
		}
		for(int i = 0 ; i <table[key].size();++i){ 
				cout<<"Sentence "<<table[key][i]  <<endl;//输出句子序号，从0开始 
				outfile<<"Sentence "<<table[key][i]  <<endl;
    			for(int j = 0; j <all[table[key][i]].size() ;++j){//输出序号为 table[key][i] 的句子 
    				cout<<all[table[key][i]][j]<<" ";
    				outfile<<all[table[key][i]][j]<<" ";
				}
			cout<<endl; 
			outfile<<endl;
		}
		cout<<endl<<"-----------------------------------------"<<endl; //进行下一次Query 
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

int getkey(string table[],string s,int n){//生成单词s在哈希表table[]中已经解决冲突的key值 
	++all_words;
	int key = myhash(s,n);
    int k = 0;
    //++search;
    while(table[(key+k*k)%n] != "" ){ //平方探测法解决冲突 
    	if(table[(key+k*k)%n] == s ) return (key+k*k)%n;//如果该单词已经在哈希表table[]中时返回该key值 
        ++k;
        //++search;
    }
    ++diff_words; 
    search+=(k+1); 
    return (key+k*k)%n; 
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

bool _read(vector<vector<string> >&all,vector<vector<int> > &table,string* hash_table, int n){ 
//将text.txt读到vector<vector<string> >&all里,all[k]表示第 k个句子 
    ifstream infile("text.txt",ios::in);
    if(!infile.is_open()) return false ;
    int i = 0;//表示第i个句子，存到all[i]里 
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
    	for(int j = 0; j <all[i].size() ;++j){
    		vector<string> ss;
    		getword(all[i][j],ss);//将字符串 all[i][j]里的所有单词提取到ss里 
    		for(int k = 0; k <ss.size();++k){
    			int key = getkey(hash_table,ss[k],n);//生成单词ss[k]的解决冲突之后的哈希值 
    			hash_table[key] = ss[k] ;
    			int h = table[key].size();
				if(h==0||table[key][h-1]!=i) 
      			table[key].push_back(i);//将该句子序号计入对应的table中 
      		}
		}
    	++i;
    }
    infile.close();
    return true;
}
 
