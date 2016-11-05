import urllib.request, urllib.parse, json, re, html, os, os.path


def pathFromUrl(url):
	if url[-1]=='/': return url;
	else: return url+'/'

class ResourceCollection:

	def __init__(self,urls):
		self.baseUrl='http://localhost:8000';
		self.resources=[]
		self.tags=[]
		self.tagsSorted=False
		self.currentResource=0
		if urls:
			for url in urls:
				if not self.resourceByUrl(url):
					self.resources.append(Resource(self,url))
		self.resources=sorted(self.resources,key=lambda res: res.label)
		for i in range(len(self.resources)):
			self.resources[i].idx=i
			
		for tag in self.tags:
			tag.dump()
	
	def _addTag(self,data,path):
		tag=self.tagByName(data['name'])
		if not tag:
			tag=Tag(self,data['name'])
			self.tags.append(tag)
		self.tagsSorted=False
		tag._addTagging(path,data)
	
	def addResource(self,url):
		if not self.resourceByUrl(url):
			self.resources[url]=Resource(self,url)
	
	def resourceByUrl(self,url):
		path=pathFromUrl(url)
		for r in self.resources:
			if r._path==path:
				return r

	def tagByName(self,name):
		for t in self.tags:
			if t.name==name:
				return t

	def sortTags(self):
		self.tags=sorted(self.tags,key=lambda tag: tag.name)
		self.tagsSorted=True

	def getTags(self):
		if not self.tagsSorted:
			self.sortTags()
		return self.tags

	def saveAll(self):
		for url in self.resources:
			self.resources[url].save()
	
		
	def getCurrentResourceIndex(self):
		return self.currentResource
		
	def getResourceCount(self):
		return len(self.resources)
		
	def getCurrentResource(self):
		if len(self.resources): return self.resources[self.currentResource]
		
	def nextResource(self):
		if self.currentResource<self.getResourceCount()-1:
			self.currentResource=self.currentResource+1
		
	def prevResource(self):
		if self.currentResource>0:
			self.currentResource=self.currentResource-1
		
	def gotoResource(self,idx):
		if idx<=0:
			self.currentResource=0
		elif idx>=len(self.resources):
			idx=len(self.resources)-1
		self.currentResource=idx
		
	def getResource(self,idx):
		if idx>=0 and idx<=len(self.resources)-1:
			return self.resources[idx]

	def getTagging(self,tagIdx):
		if tagIdx>len(self.tags)-1:
			return
		tag=self.tags[tagIdx]
		return tag.getTagging(self.getCurrentResource())
		
	def unassign(self,tagIdx):
		tag=self.tags[tagIdx]
		tag.unassign(self.getCurrentResource())
		
	def assign(self,tagIdx):
		tag=self.tags[tagIdx]
		tag.assign(self.getCurrentResource())

	def addTag(self,name,isNew=False):
		tag=Tag(self,name,isNew)
		self.tags.append(tag)
		tag.assign(self.getCurrentResource())
		
	def renameTag(self,tagIdx,name):
		if tagIdx>len(self.tags)-1:
			return
		tag=self.tags[tagIdx]
		tag.name=name
		for url in tag.taggings:
			if tag.taggings[url].state==Tag.ASSIGNED:
				res=self.resourceByUrl(url)
				res._modified=True
		
	def setComment(self,tagIdx,comment):
		tagging=self.getTagging(tagIdx)
		if tagging:
			tagging.comment=comment
			self.getCurrentResource()._modified=True
		
	def post(self,addr,data,to=0.5):
		body=json.dumps(data).encode('utf-8')
		addr=self.baseUrl+addr
		conn = urllib.request.urlopen(addr,body,timeout=to)
		r=conn.read().decode('utf-8')
		conn.close()
		r=json.loads(r)
		return r
		
	def relocateResource(self,newUrl):
		res=self.getCurrentResource()
		if newUrl[0]=='/':
			newUrl='file://'+urllib.parse.quote(newUrl)
		r=self.post('/rename/',{'url':res.getUrl(),'newUrl':newUrl,'renameDescendants':True})
		print(r)
		
		

	def getSuggestions(self,s,curTagIdx=None):
		exclude=[]
		i=0
		for tag in self.tags:
			if i==curTagIdx:
				continue
			i=i+1
			exclude.append(tag.name)
		return self.post('/suggestions/',{'prefix':s,'limit':20,'exclude':exclude},0.2)

	def save(self):
		
		data=[]
		for res in self.resources:
			if res._modified:
				isDir=0
				if res.url[:7]=='file://':
					fpath=urllib.parse.unquote(res.url[7:])
					if os.path.isdir(fpath):
						isDir=1
				tags=[]
				for tag in self.tags:
					tagging=tag.getTagging(res)
					if tagging.state==Tag.ASSIGNED:
						tags.append([tag.name,tagging.comment])
				print('ISDIR',isDir)
				data.append({'url':res.getUrl(),'tags':tags,'data':{'label':res.getLabel(),'isdir':isDir}})
		if len(data):
			r=self.post('/load/',data,5.0)

class Resource:
	
	def __init__(self,collection,url):
		self.collection=collection
		self.idx=None
		self.url=url
		if self.url[0]=='/':
			self.url='file://'+urllib.parse.quote(self.url)
		else:
			self.url=url
		self._path=pathFromUrl(self.url)
		self._modified=False
		self.load()
		
		
	def load(self):
		self.label=None
		self.description=None
		self.created_at=None
		self.modified_at=None
		self.tags=[]
		data=self.post('/resource/',{'url':self.url},2.0)
		self._modified=False
		if not data:
			self.label=self.autolabel()
			self._modified=True
		else:
			if 'label' in data: 
				self.label=data['label']
			else: 
				self.label=self.autolabel()
				self._modified=True
			if 'description' in data: self.description=data['description'] 
			if 'modified_at' in data: self.modified_at=data['modified_at']/1000.0
			if 'created_at' in data: self.created_at=data['created_at']/1000.0
			
			if '_tags' in data:
				for tag in data['_tags']:
					self.collection._addTag(tag,self._path)
			
		
	def autolabel(self):
		if self.url:
			if self.url[:4]=='http':
				try:
					conn=urllib.request.urlopen(self.url,None,timeout=3.0)
					content=conn.read(10000).decode('utf-8')
					print(content)
					m=re.search('<title>([^<]+)',content,re.IGNORECASE)
					if m:
						label=html.unescape(m.group(1))
						label=re.sub('\s+',' ',label).strip()
						return label
				except:
					pass
					
			#return urllib.parse.unquote(self.url.split('/')[-1])
		
	def save(self):
		if self.modified:
			pass
		
	def post(self,addr,data,to=0.5):
		body=json.dumps(data).encode('utf-8')
		addr=self.collection.baseUrl+addr
		conn = urllib.request.urlopen(addr,body,timeout=to)
		r=conn.read().decode('utf-8')
		conn.close()
		r=json.loads(r)
		return r
		
	def getLabel(self):                                    
		return self.label
		
	def setLabel(self,v):
		if v!=self.label:
			self.label=v
			self._modified=True
		
	def getUrl(self):
		return self.url
		
	def getIndex(self):
		return self.idx

	
class Tag:
	
	ASSIGNED=1
	NOT_ASSIGNED=0
	INHERITED=2
	
	notAssigned=None
	
	def __init__(self,collection,name,isNew=False):
		self.name=name
		self.collection=collection
		self.taggings={}
		self.assignedCount=0
		self.isNew=isNew
		if self.notAssigned is None:
			self.notAssigned=Tagging(None,None)

	def _addTagging(self,path,data):
		tagging=Tagging(path,data)
		self.taggings[path]=tagging
		if tagging.state==Tag.ASSIGNED:
			self.assignedCount=self.assignedCount+1
	
	def unassign(self,res):
		if res._path in self.taggings:
			tagging=self.taggings[res._path]
			if tagging.state==Tag.ASSIGNED:
				if tagging.inheritedFrom:
					tagging.state=Tag.INHERITED
				else:
					tagging.state=Tag.NOT_ASSIGNED
				res._modified=True
				self.assignedCount=self.assignedCount-1

	def dump(self):
		for path in self.taggings:
			tagging=self.taggings[path]

	def assign(self,res):
		if res._path in self.taggings:
			tagging=self.taggings[res._path]
			if tagging.state==Tag.NOT_ASSIGNED or tagging.state==Tag.INHERITED:
				tagging.state=Tag.ASSIGNED
				self.assignedCount=self.assignedCount+1
				res._modified=True
		else:
			self._addTagging(res._path,{'inheritedFrom':res.getUrl(),'comment':''})
			res._modified=True

	def getTagging(self,res):
		path=res._path
		if path in self.taggings:
			return self.taggings[path]
		else:
			return self.notAssigned

	def getAssignedCount(self):
		return self.assignedCount

class Tagging:
	
	def __init__(self,path,data):
		if data and path:
			inh=pathFromUrl(data['inheritedFrom'])
			if inh==path:
				self.inheritedFrom=None
				self.state=Tag.ASSIGNED
			else:
				self.inheritedFrom=data['inheritedFrom']
				self.state=Tag.INHERITED
			if 'comment' in data:
				self.comment=data['comment']
		else:
			self.inheritedFrom=None
			self.state=Tag.NOT_ASSIGNED
			self.comment=None
		

