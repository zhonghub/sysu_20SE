#include<iostream>
#include<vector>
#include<string>
using namespace std;
#include <fstream>
#include"myhash.cpp" //������ʹ�õ�hash���� 
int search; //��¼��ͬ���ʵĲ����ܴ��� 
int diff_words; //��¼��ͬ���ʵ����� 
int all_words;//��¼�������� 
int hash_k;//ѡ���ϣ���� 

int myhash(const string s,int n)//�ַ����Ĺ�ϣ�������������ʼ�Ĺ�ϣֵ 
{
	switch(hash_k){ //����hash_k��ֵѡ��ʹ�õĹ�ϣ���� 
		case 2: return myhash2(s,n);
		case 3: return myhash3(s,n);
		case 4: return myhash4(s,n);
		case 5: return myhash5(s,n);
		case 6: return myhash6(s,n);
		default: return myhash1(s,n);
	}
}
int getkey(string table[],string s,int n);//���ɵ���s�ڹ�ϣ��table[]���Ѿ������ͻ��keyֵ 
	//����õ����Ѿ��ڹ�ϣ��table[]��ʱ���ظ�keyֵ 

bool isword(char c);//�ж��ǲ�����ɵ��ʵ����ֻ���ĸ 
	
void getword(string s,vector<string>& ss); //��ȡ�ַ���s�е����е��ʵ�vector<string>&ss�� 

bool _read(vector<vector<string> >&all,vector<vector<int> > &table,string* hash_table, int n);
 //��text.txt����vector<vector<string> >&all��,all[k]��ʾ�� k������ 
//�����е��ʱ��������ɶ�Ӧ��table��hash_table 

int main(){
	cout<<"���ŵ�ַ��:  "<<endl; 
	vector<vector<string> > all;//�����о��Ӷ��� vector<vector<string> >���͵� all����,all[k]��ʾ�� k������ 
	int n = 4900 ;//hash_table������ ��Ҫ������ͬ���ʵĸ���
	cout<<"�������ϣ�������n(�Ƽ�n>=4900): "<<endl ;
	cin>>n; 
	string hash_table[n];
	//hash_tableΪ���浥�ʵĹ�ϣ��,��getkey(string table[],string s,int n)�������ɶ�Ӧ����s�����ͻ֮���keyֵ
	vector<vector<int> > table;
	//���ڴ��浥�������ڵ����о��ӵ���ţ���table[key][]�����hashֵΪkey�ĵ����������о��ӵ���� 
	vector<int> t;
	for(int i = 0 ; i <n; ++i) table.push_back(t); //��table���г�ʼ����ֵ  
	hash_k = 1;//Ĭ��ʹ��BKDRHash�㷨�Ĺ�ϣ����myhash1  
	cout<<"��ϣ����ѡ��"<<endl
	    <<"1: BKDRHash�㷨"<<endl
        <<"2: DJBHash�㷨"<<endl
		<<"3: JSHash�㷨"<<endl
		<<"4: RSHash�㷨"<<endl
		<<"5: SDBMHash�㷨"<<endl
		<<"6: ELFHash�㷨" <<endl;
	cout<<"����������1~6��ѡ���ϣ����hash_k : "<<endl;
	cin>>hash_k; //����ѡ��Ĺ�ϣ���� 
	//�����о��Ӷ��� vector<vector<string> >���͵� all����,all[k]��ʾ�� k������ 
	bool A1 = _read(all,table,hash_table,n);//��ȡtext.txt�ļ������ɶ�Ӧ��all��table��hash_table 
	ofstream outfile("answer1.txt",ios::out);//������ļ�answer.txt�� 
	cout<<"all sentences: "<<all.size()<<endl;
	cout<<"all_words: "<<all_words<<endl;
	cout<<"diff_words: "<<diff_words<<endl;
	cout<<"search: "<<search<<endl;
	cout<<"space = n : "<<n<<endl;
	cout<<"n/diff_words: "<<(double)n/(double)diff_words<<endl;
	cout<<"average_search = search/diff_words: "<< (double)search/(double)diff_words <<endl;
	cout<<"-----------------------------------------"<<endl;
	cout<<"You can use '$stop' to stop the Query !"<<endl; 
	cout <<"Query :"<<endl; //�������� and �� amu  ��û�н����ͻʱhashֵ��ͬ 
	cout<<"������: "; 
	outfile<<"���ŵ�ַ��:  "<<endl; 
	outfile<<"�������ϣ�������n(�Ƽ�n>=4900): "<<endl<<n<<endl ;
	outfile<<"��ϣ����ѡ��"<<endl
	    <<"1: BKDRHash�㷨"<<endl
        <<"2: DJBHash�㷨"<<endl
		<<"3: JSHash�㷨"<<endl
		<<"4: RSHash�㷨"<<endl
		<<"5: SDBMHash�㷨"<<endl
		<<"6: ELFHash�㷨" <<endl;
	outfile<<"����������1~6��ѡ���ϣ����hash_k : "<<endl<<hash_k<<endl;
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
	outfile<<"������: "; 
	string find;//Ҫ��ѯ�ĵ��� 
	while(cin>>find && find!="$stop"){ //��������ĵ��ʽ�����Ӧ�������ѯ���˳� 
		outfile<<find<<endl; 
		int key = getkey(hash_table,find,n);
		if(table[key].size()==0){//�õ���find�����ڶ�Ӧ�ľ���ʱ 
			cout<<"There is not the word!"<<endl;
			outfile<<"There is not the word!"<<endl;
		}
		for(int i = 0 ; i <table[key].size();++i){ 
				cout<<"Sentence "<<table[key][i]  <<endl;//���������ţ���0��ʼ 
				outfile<<"Sentence "<<table[key][i]  <<endl;
    			for(int j = 0; j <all[table[key][i]].size() ;++j){//������Ϊ table[key][i] �ľ��� 
    				cout<<all[table[key][i]][j]<<" ";
    				outfile<<all[table[key][i]][j]<<" ";
				}
			cout<<endl; 
			outfile<<endl;
		}
		cout<<endl<<"-----------------------------------------"<<endl; //������һ��Query 
		cout<<"You can use '$stop' to stop the Query !"<<endl; 
		cout<< "Query :"<<endl;
		cout<<"������: "; 
		outfile<<endl<<"-----------------------------------------"<<endl;
		outfile<<"You can use '$stop' to stop the Query !"<<endl; 
		outfile<< "Query :"<<endl;
		outfile<<"������: "; 
	}
	outfile.close();
	return 0;
}
//����Ϊ����ʵ�� 

int getkey(string table[],string s,int n){//���ɵ���s�ڹ�ϣ��table[]���Ѿ������ͻ��keyֵ 
	++all_words;
	int key = myhash(s,n);
    int k = 0;
    //++search;
    while(table[(key+k*k)%n] != "" ){ //ƽ��̽�ⷨ�����ͻ 
    	if(table[(key+k*k)%n] == s ) return (key+k*k)%n;//����õ����Ѿ��ڹ�ϣ��table[]��ʱ���ظ�keyֵ 
        ++k;
        //++search;
    }
    ++diff_words; 
    search+=(k+1); 
    return (key+k*k)%n; 
}

bool isword(char c){ //�ж��ǲ�����ɵ��ʵ����ֻ���ĸ 
	if((int)c>=48 && (int)c <=57) return true;
	else if((int)c>=65 && (int)c <=90) return true;
	else if((int)c>=97 && (int)c <=122) return true;
	else return false;
}
void getword(string s,vector<string>& ss){ //��ȡ�ַ���s�е����е��ʵ�vector<string>&ss�� 
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
//��text.txt����vector<vector<string> >&all��,all[k]��ʾ�� k������ 
    ifstream infile("text.txt",ios::in);
    if(!infile.is_open()) return false ;
    int i = 0;//��ʾ��i�����ӣ��浽all[i]�� 
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
    		getword(all[i][j],ss);//���ַ��� all[i][j]������е�����ȡ��ss�� 
    		for(int k = 0; k <ss.size();++k){
    			int key = getkey(hash_table,ss[k],n);//���ɵ���ss[k]�Ľ����ͻ֮��Ĺ�ϣֵ 
    			hash_table[key] = ss[k] ;
    			int h = table[key].size();
				if(h==0||table[key][h-1]!=i) 
      			table[key].push_back(i);//���þ�����ż����Ӧ��table�� 
      		}
		}
    	++i;
    }
    infile.close();
    return true;
}
 
