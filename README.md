
Mount your trainingset folder for MALLET into `/data` when running this
container using the `--volume` option: `--volume path/to/trainingset:/data/`  


assumed folder structure for your trainingset:
```
path/to/trainingset
├── processed
│   └── corpus.mallet
├── stoplist.txt
└── topics
    ├── inferencer
    └── keys.txt
```
