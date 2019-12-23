

CanvasExt={

    layerName: "layer",
    layer: 0,    
    is_drag: false,
    image_src:"",
    image_width:0,
    image_height:0,
    sourceX:0,
    sourceY:0,

    getCurrentLayerNameAndIncr:function(){
        var name =  this.layerName + this.layer;
        this.layer++;
        return name;
    },
    getCurrentLayerNameDesc:function(){
        if(this.layer>0){
           this.layer--;
        }
        var name =  this.layerName + this.layer;
        return name;
    },

    getCurrentLayerName:function(){
        var name =  this.layerName + this.layer;
        return name;
    },

    drawImage:function(canvasId,img_url,w,h){
      this.image_src = img_url;
      this.image_width = w;
      this.image_height = h;

      $('#'+canvasId).drawImage({
          layer:true,
          name:"image",
          source: img_url,
          width:w,
          height:h,
          x: 0, y: 0,
          fromCenter: false
        });
    },



    drawPen:function(canvasId,penColor,penWidth,context){
                var that=this;

                that.penColor=penColor;
                that.penWidth=penWidth;
                //canvas DOM对象  
                var canvas=document.getElementById(canvasId);
                //canvas 的矩形框
                var canvasRect = canvas.getBoundingClientRect();

                //矩形框的左上角坐标
                var canvasLeft=canvasRect.left;
                var canvasTop=canvasRect.top;

                //画图坐标原点
                
                that.is_drag = false;
                

                //鼠标点击按下事件，画图准备
                canvas.onmousedown=function(e){

                    
                    if(that.is_drag){
                      return;
                    }
                    //设置画笔颜色和宽度
                    var color=that.penColor;
                    var width=that.penWidth;

                    //设置原点坐标
                      
                    var wtop = $(window).scrollTop();
                    that.sourceX=e.offsetX-canvasLeft;       
                    that.sourceY=e.offsetY+100-canvasTop;        


                    //鼠标移动事件，画图
                    canvas.onmousemove=function(e){

                        var r_layerName=that.getCurrentLayerNameAndIncr();

                        console.log(r_layerName);
                        //当前坐标
                        var wtop = $(window).scrollTop();
                        var currX=e.offsetX-canvasLeft;
                        var currY=e.offsetY+100-canvasTop;

                        //画线
                        $("#"+canvasId).drawLine({
                          layer:true,
                          name:r_layerName,
                          strokeStyle: color,
                          strokeWidth: width,
                          x1: that.sourceX, y1: that.sourceY,
                          x2: currX,
                          y2: currY
                        })

                        //$("#"+canvasId).saveCanvas();

                        //设置原点坐标
                        that.sourceX=currX;
                        that.sourceY=currY;
                    }
            }
            //鼠标没有按下了，画图结束
            canvas.onmouseup=function(e){
                //$("#"+canvasId).drawLayers()
                //$("#"+canvasId).saveCanvas();
                canvas.onmousemove=null;
                //context.save();
                //console.log("save");
            }

    },

   clearPen:function(canvasId){
      //var canvas=document.getElementById(canvasId);
      this.is_drag = false;
   },

   restoreCanvas:function(canvasId){

      for(var i=0;i<10;i++){
        var r_layerName=this.getCurrentLayerNameDesc();
        console.log("restore:"+r_layerName);
        $("#"+canvasId).removeLayer(r_layerName).drawLayers();
      }
      console.log("restore");
   },

   clearCanvas:function(canvasId){

      $("#"+canvasId).removeLayers();
      $("#"+canvasId).clearCanvas();
      layer=0;

      this.drawImage(canvasId,this.image_src,this.image_width,this.image_height);
      console.log("clear");
   },

    setPenColor:function(penColor){
         this.penColor=penColor;
    },

    setPenWidth:function(width){
         this.penWidth=width;
    },

    getImage:function(canvasId){
      var img = $("#"+canvasId).getCanvasImage('png');
      return img;
    },

    drawText:function(canvasId,text,color,yy){
      var that=this;
      this.is_drag = true;

      var r_layerName= this.getCurrentLayerNameAndIncr();
      $("#"+canvasId).drawText({
        layer:true,
        name:r_layerName,
        draggable: true,
        bringToFront: true,
        fillStyle: color,
        strokeStyle: color,
        strokeWidth: 1,
        x: 60, 
        y: yy,
        fontSize: 24,
        fontFamily: "PingFang SC,Microsoft YaHei,SimHei,Arial,SimSun",
        text: text
      })


    }

    
}

//https://projects.calebevans.me/jcanvas/docs/getCanvasImage/
