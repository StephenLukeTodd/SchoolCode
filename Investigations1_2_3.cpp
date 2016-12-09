#include <iostream>
#include <string>
using namespace std;

///Stephen Luke Todd 
///Investigations 1, 2, 3 for Homework 1. 


void PrintingArrays(int arrays[], int size)
 {
    for ( int i = 0; i < size; i++ ) 
    {
        cout << arrays[i] << ' ';
    }
    cout << endl;
}

void PassbyReference(int* array, size_t ArraySize) 
{ 
  for (size_t i = 0; i < ArraySize; ++i) 
  { 
    std::cout << array[i] << " "; 
  } 
  std::cout << std::endl; 
} 





int main()
{
    cout<< "Investigations1: Showing how variable scoping is shown in brackets." << endl; 
    cout << "Investigation Number 1. Variable Scope handling." << endl; 
    cout << endl;
    int nest1 = 0;
    cout << "Nest1 at declaration: " << nest1 << endl;
    cout << endl; 

    {
        int nest2 = 0;
        nest1 = nest1 + 1;
        cout << "Nest2 at declaration: " << nest2 << endl; 
        cout << "Nest1 in Nest2: " << nest1 << endl; 
        cout << endl; 
        
        {
            int nest3 = 0; 
            nest1 = nest1 + 1; 
            nest2 = nest2 + 1; 
            cout << "Nest3 at declaration: " << nest3 << endl; 
            cout << "Nest1 in Nest3: " << nest1 << endl; 
            cout << "Nest2 in Nest3: " << nest3 << endl; 
            cout << endl; 

            for(int j = 1; j < 10; j++)
            {
                nest3 = nest3 + 1; 
                nest2 = nest2 + 1;
                nest1 = nest1 + 1;

                cout << "Nest1 in for-loop: " << nest1 << endl; 
                cout << "Nest2 in for-loop: " << nest2 << endl; 
                cout << "Nest3 in for-loop: " << nest3 << endl; 
                cout << endl; 
            }
        }
        
    }
    

    cout << "Investigation 2: Arrays are usually passed by function in C++," << endl;
    cout << "Normally, a pointer to the first element is passed by value." << endl; 
    cout << "The size of the array is lost in this process and must be passed separately." << endl;
    cout << endl;
    cout << endl; 
    cout << "Investigation 2: Passing by Reference" << endl; 
    int arrays[] = { 5, 7, 8, 9, 1, 2 };
    PrintingArrays(arrays, 6);


    cout << endl;
    cout << "Invetigation 2: Passing by Value" << endl;  
    int array[10] = {0,1,2,3,4,5,6,7,8,9}; 
    PassbyReference(array, sizeof(array)/sizeof(int));

    cout << endl; 
    cout << endl;     
    cout << "Investigation 3: It will go straight to a specific point in" << endl; 
    cout << "the program." << endl;

    for (int i = 1; i < 10; i--)
        {
            cout << "First for-loop." << endl; 
            cout << endl;

            for(int j = 2; j < 10; j--)
                {
                    cout << "Second for-loop." << endl;
                    cout << "Value of i:" << i << endl; 
                    cout << "Value of j: "<< j << endl; 
                    cout << endl; 
                    if (j == -10)
                    {
                        cout << "Once the condition is reached: get out of the loop" << endl; 
                        cout << "by goto final. " << endl;
                        cout << endl; 
                        goto final; 
                    }

                }
        }
        final: 

    cout << "Went to here." << endl; 




}
