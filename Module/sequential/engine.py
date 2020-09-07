import faiss
from datetime import datetime,timedelta

class FlatL2Engine:
    def __init__(self, feature,device=-1):
        print('Construct Flat L2 Index')
        self.cnt = feature.shape[0]
        self.index=faiss.IndexFlatL2(feature.shape[1])
        if device!='-1':
            res = faiss.StandardGpuResources()
            self.index=faiss.index_cpu_to_gpu(res, device, self.index)
        self.index.add(feature)


    def search(self, feature, topk):
        start=datetime.now()
        return self.index.search(feature, min(self.cnt,topk)),(datetime.now()-start).total_seconds()
