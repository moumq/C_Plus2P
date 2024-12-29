#include <iostream>
using namespace std;

void BubbleSort(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
	{
			//如果用一个flag来判断当前数组是否已经有序,有序则退出循环
			bool flag = true;
            for (int j = 0; j < n - i - 1; j++)
	        {
                    if (arr[j] > arr[j + 1]) 
					{
                            int temp = arr[j];
                            arr[j] = arr[j + 1];
                            arr[j + 1] = temp;
                            flag = false;
                     }
             }
             if (flag) break;
     }
}


void SelectionSort(int a[],int len)
{
	for(int i = 0; i < len; i++)
	{
		int min = i;
		for(int j = i + 1; j < len; j++)
		{
			if(a[j] < a[min])
			min = j;
		}
		int temp = a[min];
		a[min] = a[i];
		a[i] = temp;
	}
}

void insertSort(int a[], int n)
{
   for(int i = 1; i < n; i++)
   {
	  if(a[i] < a[i-1])
	  {
	      int j = i-1;     
          int x = a[i]; 
	      while(j >= 0 && x < a[j]) 
	      {
             a[j+1] = a[j]; 
	         j--;
	      }
	      a[j+1] = x;  
	  }   
   }
}

void Quicksort(int arr[], int low, int high) {
	if (low < high) {
		int i = low;
		int j = high;
		int key = arr[i];
		while (i < j) {
			while (i < j && arr[j] >= key)
				j--;
			if (i < j) arr[i] = arr[j];
			while (i < j && arr[i] <= key)
				i++;
			if (i < j) arr[j] = arr[i];
		}
		arr[i] = key;
		Quicksort(arr, low, i - 1);
		Quicksort(arr, i + 1, high);
	}
}

const int MAX = 10000;

int main(){
    int arr[MAX]={0};
    int n=0;
    cin>>n;
    for(int i=0;i<n;i++){
        cin>>arr[i];
    }

    BubbleSort(arr,n);

    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;

    SelectionSort(arr,n);

    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;

    insertSort(arr,n);

    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;

    Quicksort(arr,0,n-1);

    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<endl;
    return 0;
}