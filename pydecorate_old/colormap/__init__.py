import numpy as np
from PIL import Image
import ImageDraw

class ColorScaleItem(object):
      value=None
      color=None
      interpol="lin"
      name=""
      
      def __init__(self,value=None,color=None,interpol="lin",name=""):
            self.value=float(value)
            self.color=color
            self.interpol=interpol
            self.name=name
      def setColor(self,color_tub):
            self.color=color_tub
      def getColor255(self):
            r=int(self.color[0]*255)
            g=int(self.color[1]*255)
            b=int(self.color[2]*255)
            return (r,g,b)
        
class ColorMap(object):
      scale_items=None
      below_extend=None
      above_extend=None
      scale_items_dict=None
      enhance=None

      def __init__(self, scale=None, colors=None, values=None,enhance=None):

            # parse input
            if scale != None:
                  self.scale_items=[]
                  for val in scale.keys():
                        col=scale[val][0]
                        inp=scale[val][1]
                        self.scale_items.append(ColorScaleItem(value=val,color=col,interpol=inp))

            elif values != None:
                  self.scale_items=[]
                  nval=len(values)
                  for i in range(nval):
                        shade=float(i)/(nval-1)
                        self.scale_items.append(ColorScaleItem(value=values[i],color=(shade,shade,shade)))

            elif colors != None:
                  self.scale_items=[]
                  nval=len(colors)
                  for i in range(nval):
                        value=float(i)/(nval-1)
                        self.scale_items.append(ColorScaleItem(value=value,color=colors[i]))
                  

            # build dict
            self._build_dict()

            # init extends
            if self.scale_items is None:
                  return
            else:
                  (mi,ma)=self.minmaxValue()
                  self.below_extend = ColorScaleItem(value=float('-inf'),color=self.scale_items_dict[mi].color,name="-inf")
                  self.above_extend = ColorScaleItem(value=float('+inf'),color=self.scale_items_dict[ma].color,name="+inf")
            
            # set enhancement behaviour
            self.enhance=enhance

            
      def values(self):
            vals=[]
            if self.scale_items != None:
                  for i in range(len(self.scale_items)):
                        vals.append(self.scale_items[i].value)
            return sorted(vals)

      def conValues(self):
            vals=[]
            if self.scale_items != None:
                  for i in range(len(self.scale_items)):
                        if self.scale_items[i].interpol in ["con",""]:
                              vals.append(self.scale_items[i].value)
            return sorted(vals)

      def minmaxValue(self):
            if self.scale_items is None:
                  return (None,None)
            else:
                  vals=self.values()
                  return (vals[0],vals[-1])

      def _build_dict(self):
            if self.scale_items != None:
                  self.scale_items_dict={}
                  for si in self.scale_items:
                        self.scale_items_dict[si.value]=si

      def _color255(self,color):
            r = int(round(color[0]*255.0))
            g = int(round(color[1]*255.0))
            b = int(round(color[2]*255.0))
            return (r,g,b)
    
      def _create_checker_rgb(self,size,color1=(0,0,0),color2=(1,1,1),check_size=10):
            # checker pattern
            (nx,ny)=size
            d=2*check_size
            ind=np.indices((ny,nx))
            chk=np.zeros((ny,nx),dtype=np.uint8)
            chk[((ind[0]%d)>(d/2-1))!=((ind[1]%d)>(d/2-1))]=1
            # color and combine into image
            r=np.array(chk)
            g=np.array(chk)
            b=np.array(chk)
            sel=(chk==0)
            r[sel]=(int(round(color2[0]*255)))
            g[sel]=(int(round(color2[1]*255)))
            b[sel]=(int(round(color2[2]*255)))
            sel=(chk==1)
            r[sel]=(int(round(color1[0]*255)))
            g[sel]=(int(round(color1[1]*255)))
            b[sel]=(int(round(color1[2]*255)))
            return (r,g,b)

      def _create_checker_image(self,size,color1=(0,0,0),color2=(1,1,1),check_size=10):
            (r,g,b)=self._create_checker_rgb(size=size,color1=color1,color2=color2,check_size=check_size)
            tr=Image.fromarray(r)
            tg=Image.fromarray(g)
            tb=Image.fromarray(b)
            img=Image.merge('RGB',(tr,tg,tb))
            return img
        
      def color_scale_image(self,size,minmax=None,nan_color=(1.0,1.0,1.0),nan_check_color=(1,1,1),nan_check_size=0):
            # get color map range
            (mi,ma)=self.minmaxValue()
            # create range of values
            #values=np.arange(mi,ma,((ma-mi)/size[0]))
            values=np.indices(size)[0].transpose()*((ma-mi)/size[0])+mi
            # map scale to image
            img=self.map_to_image(values,minmax=minmax,
                                  nan_color=nan_color,nan_check_color=nan_check_color,
                                  nan_check_size=nan_check_size)
            return img

      def map_to_image(self,arr_inn,minmax=None,nan_color=(0,0,0),nan_check_color=(1,1,1),nan_check_size=0):
            # get color map range
            #(mi,ma)=self.minmaxValue()
            #if minmax is not None:
            #      (mi,ma)=minmax
            # map input values
            (r,g,b)=self.map(arr_inn)
            nans=np.isnan(r)
            r[nans]=float(nan_color[0])
            g[nans]=float(nan_color[1])
            b[nans]=float(nan_color[2])
            # generate PIL image layer
            rB=np.array(r*255.0,np.uint8)
            gB=np.array(g*255.0,np.uint8)
            bB=np.array(b*255.0,np.uint8)
            tr=Image.fromarray(rB)
            tg=Image.fromarray(gB)
            tb=Image.fromarray(bB)
            img=Image.merge('RGB',(tr,tg,tb))
            # nan img mask
            if nan_check_size>0:
                  checks=self._create_checker_image(img.size,
                                                    color1=nan_color,
                                                    color2=nan_check_color,
                                                    check_size=nan_check_size)
                  nanimg=Image.fromarray(np.array(nans,dtype=np.uint8)*255)
                  img=Image.composite(checks,img,nanimg)
            return img

      def rescale_values(self,new_min,new_max):
            (old_min,old_max)=self.minmaxValue()
            old_D=old_max-old_min
            new_D=new_max-new_min
            for item in self.scale_items:
                  item.value=(item.value-old_min)*new_D/old_D+new_min
            self._build_dict()

      def add_to_values(self,value):
            for item in self.scale_items:
                  item.value=item.value+value
            self._build_dict()

      def _apply_enhancement(self,arr):
            if self.enhance == "normalize":
                  not_nans = ~np.isnan(arr)
                  self.rescale_values(arr[not_nans].min(),arr[not_nans].max())
            self.enhance=None

      def map(self,arr_inn):
            # deal with enhancement
            self._apply_enhancement(arr_inn)
            # handle masked array
            if hasattr(arr_inn,'mask'):
                  mask=arr_inn.mask
            else:
                  mask=np.zeros(arr_inn.shape,dtype=np.bool)

            # construct rgb space
            r=arr_inn.copy()
            r[r==r]=0.0
            g=r.copy()
            b=r.copy()
            # color
            # color extends
            mm=self.minmaxValue()
            if self.below_extend:
                  r[arr_inn<mm[0]]=self.below_extend.color[0]
                  g[arr_inn<mm[0]]=self.below_extend.color[1]
                  b[arr_inn<mm[0]]=self.below_extend.color[2]
            else:
                  r[arr_inn<mm[0]]=np.nan
                  g[arr_inn<mm[0]]=np.nan
                  b[arr_inn<mm[0]]=np.nan
            if self.above_extend:
                  r[arr_inn>mm[1]]=self.above_extend.color[0]
                  g[arr_inn>mm[1]]=self.above_extend.color[1]
                  b[arr_inn>mm[1]]=self.above_extend.color[2]
            else:
                  r[arr_inn>mm[1]]=np.nan
                  g[arr_inn>mm[1]]=np.nan
                  b[arr_inn>mm[1]]=np.nan

            # scale
            vals=self.values()
            for i in range(len(vals)-1):
                  si0=self.scale_items_dict[vals[i]]
                  si1=self.scale_items_dict[vals[i+1]]

                  val0=vals[i]
                  val1=vals[i+1]
                  dval=abs(val1-val0)

                  r0,g0,b0=si0.color
                  r1,g1,b1=si1.color

                  dr=r1-r0
                  dg=g1-g0
                  db=b1-b0

                  if si0.interpol=="lin":
                        r[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = r0 \
                            +(arr_inn[(arr_inn>=si0.value)&(arr_inn<=si1.value)]-val0)*dr/dval
                        g[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = g0 \
                            +(arr_inn[(arr_inn>=si0.value)&(arr_inn<=si1.value)]-val0)*dg/dval
                        b[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = b0 \
                            +(arr_inn[(arr_inn>=si0.value)&(arr_inn<=si1.value)]-val0)*db/dval

                  if si0.interpol=="con":
                        r[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = si0.color[0]
                        g[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = si0.color[1]
                        b[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = si0.color[2]

                  if si0.interpol=="":
                        r[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = np.nan
                        g[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = np.nan
                        b[(arr_inn>=si0.value)&(arr_inn<=si1.value)] = np.nan
                        r[(arr_inn==si0.value)] = si0.color[0]
                        g[(arr_inn==si0.value)] = si0.color[1]
                        b[(arr_inn==si0.value)] = si0.color[2]
                  if "gamma" in si0.interpol:
                        gamma=float(si0.interpol.split(' ')[1])
                        sel=(arr_inn>=si0.value)&(arr_inn<=si1.value)
                        r[sel]=r0+dr*((arr_inn[sel]-val0)/dval)**(1.0/gamma)
                        g[sel]=g0+dg*((arr_inn[sel]-val0)/dval)**(1.0/gamma)
                        b[sel]=b0+db*((arr_inn[sel]-val0)/dval)**(1.0/gamma)

                        

            # apply masked values
            r[mask]=np.nan
            g[mask]=np.nan
            b[mask]=np.nan

            return (r,g,b)

class Compositor(object):
      colormaps=None
      method=None

      def __init__(self,colormaps,method="add"):
            self.colormaps=colormaps
            self.method=method
    
      def map_to_image(self,arrays,minmax=None,
                       nan_colors=None,
                       nan_color=(0,0,0),
                       nan_check_color=(1,1,1),nan_check_size=0):
            # map input values
            r=np.zeros(arrays[0].shape)
            g=r.copy()
            b=r.copy()
            nans=True
            for i in range(len(arrays)):
                  arr=arrays[i]
                  colormap=self.colormaps[i]
                  (rc,gc,bc)=colormap.map(arr)
                  # color nan areas of this layer
                  nan=np.isnan(rc)
                  if nan_colors is None:
                        nancol=(0,0,0)
                  else:
                        nancol=nan_colors[i]
                  rc[nan]=float(nancol[0])
                  gc[nan]=float(nancol[1])
                  bc[nan]=float(nancol[2])
                  # accumulate nans
                  nans=nans&nan
                  # composite this layer
                  if self.method=="add":
                        r+=rc
                        g+=gc
                        b+=bc
                  elif self.method=="over":
                        valid=~nan
                        r[valid]=rc[valid]
                        g[valid]=gc[valid]
                        b[valid]=bc[valid]
            # normalize colors to range [0,1]
            r=r/r.max()
            g=g/g.max()
            b=b/b.max()
            # generate PIL image layer
            rB=np.array((r)*255.0,np.uint8)
            gB=np.array((g)*255.0,np.uint8)
            bB=np.array((b)*255.0,np.uint8)
            tr=Image.fromarray(rB)
            tg=Image.fromarray(gB)
            tb=Image.fromarray(bB)
            img=Image.merge('RGB',(tr,tg,tb))
            # nan img mask
            if nan_check_size>0:
                  checks=self.colormaps[0]._create_checker_image(img.size,
                                                    color1=nan_color,
                                                    color2=nan_check_color,
                                                    check_size=nan_check_size)
                  nanimg=Image.fromarray(np.array(nans,dtype=np.uint8)*255)
                  img=Image.composite(checks,img,nanimg)

            return img


def Red(**kwargs):
      return ColorMap(colors=[(0,0,0),(1,0,0)],**kwargs)
def Green(**kwargs):
      return ColorMap(colors=[(0,0,0),(0,1,0)],**kwargs)
def Blue(**kwargs):
      return ColorMap(colors=[(0,0,0),(0,0,1)],**kwargs)
