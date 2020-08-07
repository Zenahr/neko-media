# Software Architecture

**Base architecture:** Database powered web app

## Components

### Frontend

Click on an Episode Card and this happens: https://stackoverflow.com/questions/18246053/how-can-i-create-a-link-to-a-local-file-on-a-locally-run-web-page

### Backend

#### API

Type: Restful API

Database: non-relational (document based). See [this video](https://youtu.be/5j-xvNtAZQ8)

##### User Model

Query questions:

- How much time have I spent watching media in total?

---

items are Media Items
Media Items can either be

- Standalone

or

- Compound


##### Standalone Model
(OVA for example)
Query questions:

- What is the movie called?
- When has it been added to the media library? (created_at)
- What is the full local media file path?
- What is the full local thumbnail file path?
- How much of the media have I watched already?
- How many times have I watched the media from start to finish?

Representation:
```json

```

##### Compound Model
(Series for example)
Compounds have multiple Children

Representation:
```json
```