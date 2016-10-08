#DuDuLu

[中文](README-CHINEXE.md)
-----------

![logo](pic/logo.png)

##Introduction

DuDuLu is a web api server used to text mining.Support some api to get basic information from text presently.I will update it when it need.

As the same time,this project was collected my another repositories.

[ML and DM in action](https://github.com/MashiMaroLjc/ML-and-DM-in-action)

##Version

> 0.1.1

> The first number mean the version of reconstruction.The second one mean the version of
functional.The last one mean the version of fixing bug or functional optimization.


##API Introduction

- API of cut the sentence: /cut?sentence=""&method=""
 
 - sentence  a sentence you need to cut
 - method=all ALL MODEL to cut sentence
 - method=defaule Defalue MODEL to cut sentence
 - method=search HMM MODEL to cut sentence
 - method=search_all HMM MODEL and ALL MODEL to cut sentence
 - when you aren't support the method name,it was defalue model.


 Return a data with JSON format.Just like 

```
 {
 	"status" //successful or failure 
 	"info" //The information only exist when the status is failure.It will be null,when the query successful.
 	"data"://The word list which cut from the sentence. 
 }
```




- Word Count Api: /count?sentence=""&method=""
 
 - The parmas same as API of cut the sentence.

  Return a data with JSON format.Just like 

```
 {
 	"status" //successful or failure 
 	"info" //The information only exist when the status is failure.It will be null,when the query successful.
 	"data"://A Hash Table .Key is the word and the value is the frequency. 
 }
```


- Mood Analysze Api  /mood?sentence=""

 - sentence  A sentence with 1 to 200 words.

   Return a data with JSON format.Just like 

```
 {
 	"status" //successful or failure 
 	"info" //The information only exist when the status is failure.It will be null,when the query successful.
 	"data"://A Hash Table .Key is three names of mood, positive,neutral,negative.Value is the possibility of three moods. 
 }
```

Currently only support Chinese

##Request

+ python 3.4+
+ flask 0.10.1
+ jieba 0.38
+ numpy 


##How to use

```git clone``` or download the code from this page,and input ```python dudulu.py``` in correct directory.

And visited  ```localhost:8888``` on your brower,your can visited the page that used to test
the api ,which used to analyze the mood from text

##ToDoList
- [x] As far as possible,use the script to finish the train of model.
- [x] Improved algorithm.
- [ ] Let User train the model together.

##Demo

[My api server](http://119.29.175.45:8888/)

##Example

![1](pic/1.png)
![2](pic/2.png)
![3](pic/3.png)
![4](pic/4.png)