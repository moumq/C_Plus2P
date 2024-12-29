#include <iostream>
#include <vector>
using namespace std;

vector<int> Next(string pattern)
{
	vector<int> next;
	next.push_back(0);	
	for (int i = 1, j = 0; i < pattern.length(); i++)
	{
		while (j > 0 && pattern[j] != pattern[i])
		{ 
			j = next[j - 1];
		}
		if (pattern[i] == pattern[j])
		{
			j++; 
		}
		next.push_back(j);
	}
	return next;
}

int main()
{
	string pattern = "abc", target = "abc";
    cin >> pattern >> target;
	vector<int>next = Next(pattern);

	for (int i = 0, j = 0; i < target.length(); i++)
	{
		while (j > 0 && target[i] != pattern[j])
		{
			j = next[j - 1];
		}
		if (target[i] == pattern[j])
		{
			j++;
		}
		if (j == pattern.length())
		{
			cout <<  i - j  << endl;
			j = next[j - 1];
		}
	}
	return 0;
}
