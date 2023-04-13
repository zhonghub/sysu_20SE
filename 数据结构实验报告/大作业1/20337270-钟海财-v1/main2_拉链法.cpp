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

struct word{
	string s;
	vector<int> index;//���浥��s���ڵľ��ӵ���� 
}; 

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

int getkey(vector<vector<word*> > &table,string s,int n);
//����ʹ�������������ͻ�����ص���s�ڹ�ϣ��table[myhash(s)][]�е�λ�� 

bool isword(char c);//�ж��ǲ�����ɵ��ʵ����ֻ���ĸ 
	
void getword(string s,vector<string>& ss); //��ȡ�ַ���s�е����е��ʵ�vector<string>&ss�� 

bool _read(vector<vector<string> >&all,vector<vector<word*> > &table, int n);
 //��text.txt����vector<vector<string> >&all��,all[k]��ʾ�� k������ 
//�����е��ʱ��������ɶ�Ӧ��table

int main(){
	vector<vector<string> > all;//�����о��Ӷ��� vector<vector<string> >���͵� all����,all[k]��ʾ�� k������ 
	cout<<"������:  "<<endl;
	int n = 5000 ;//table������ ������ʹ��������������С�ڲ�ͬ���ʵĸ��� 
	cout<<"�������ϣ�������n:(�Ƽ�n>=100) "<<endl ;
	cin>>n; 
	vector<vector<word*> > table;//���浥�����ھ�����ţ��絥��s��key = getkey(table,s,n),
	//���ھ�����Ŵ�����table[myhash[s]][key]->index[]�� 
	vector<word*> t;
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
	cin>>hash_k;//ѡ��ʹ�õĹ�ϣ���� 
	//�����о��Ӷ��� vector<vector<string> >���͵� all����,all[k]��ʾ�� k������ 
	bool A1 = _read(all,table,n);//��ȡtext.txt�����ɶ�Ӧ��all��table
	ofstream outfile("answer2.txt",ios::out);//������ļ�answer.txt��
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
	outfile<<"������:  "<<endl; 
	outfile<<"�������ϣ�������n:(�Ƽ�n>=100) "<<endl<<n<<endl ;
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
	string find; 
	while(cin>>find&&find!="$stop"){//��������ĵ��ʽ�����Ӧ�������ѯ���˳� 
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

int getkey(vector<vector<word*> > &table,string ss,int n){//���ɵ���s�ڹ�ϣ��table[key1]�����е����� 
	++all_words;
	int key1 = myhash(ss,n);
    int h= table[key1].size();
    for(int i = 0 ; i < h;++i){ //������ 
    	if(table[key1][i]->s == ss) return i;//����õ����Ѿ��ڹ�ϣ��table[]��ʱ���ظ�keyֵ 
    }
    search+=(h+1);
    ++diff_words; 
    return h; 
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

bool _read(vector<vector<string> >&all,vector<vector<word*> > &table, int n){ 
//��text.txt����vector<vector<string> >&all��,all[k]��ʾ�� k������ 
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
    	for(int j = 0; j <all[i].size() ;++j){ //�Ե�i������all[i]��ȡ���е��ʲ��浽��ϣ���� 
    		vector<string> ss;
    		getword(all[i][j],ss);//���ַ��� all[i][j]������е�����ȡ��ss�� 
    		for(int k = 0; k <ss.size();++k){
    			int key1 = myhash(ss[k],n);
    			int key2 = getkey(table,ss[k],n);//���ɵ���words[k]�Ľ����ͻ֮��Ĺ�ϣֵ 
    			if(key2==table[key1].size()){
    			word *t0 = new word;
    			t0->s = ss[k] ;
				table[key1].push_back(t0);
				}
				int h = table[key1][key2]->index.size();
      			if(h==0||table[key1][key2]->index[h-1]!=i) //����þ���δ����¼
				  table[key1][key2]->index.push_back(i);//���þ�����ż����Ӧ��table�� 
      		}
		}
    	++i;
    } 
    infile.close();
    return true;
}


