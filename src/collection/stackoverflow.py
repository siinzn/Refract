"""

There was an attempt to have a script for this process, but since it was taking too much time of mine i decided to go
with the sql query approach which lets me get data from stack overflow from this website : 
https://data.stackexchange.com -> Click Stack Overflow -> Compose Query -> Paste the below SQL Query. 

NOTE: This sql query was made using AI i am not capable of SQL LMAOO

SELECT TOP 30000
    ans.Id AS answer_id,
    ans.CreationDate AS created_at,
    ans.Score AS score,
    ans.Body AS body,
    parent.Title AS question_title,
    parent.Tags AS tags
FROM Posts ans
INNER JOIN Posts parent ON ans.ParentId = parent.Id
WHERE 
    ans.PostTypeId = 2
    AND ans.Score >= 10
    AND (
        parent.Tags LIKE '%<c++>%'
        OR parent.Tags LIKE '%<systems-programming>%'
        OR parent.Tags LIKE '%<linux-kernel>%'
        OR parent.Tags LIKE '%<memory-management>%'
        OR parent.Tags LIKE '%<posix>%'
        OR parent.Tags LIKE '%<syscall>%'
        OR parent.Tags LIKE '%<operating-system>%'
        OR parent.Tags LIKE '%<compiler>%'
        OR parent.Tags LIKE '%<multithreading>%'
    )
ORDER BY ans.Score DESC

"""

