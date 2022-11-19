## Create tables
```sql
create table users (
uid varchar(255), 
name varchar(255), 
email varchar(255), 
password varchar(255),
role int,
language varchar(255)
)
```


```sql
create table ticket (
uid varchar(255), 
author varchar(255), 
title varchar(255),
description varchar(255),
priority int,
status int,
)
```