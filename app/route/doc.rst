在介绍api之前，先描述下数据库中与之相关的表，关于数据本身

主要涉及的操作关乎三张表

eh_launch_pad_layouts，存储所有layout数据

eh_banners，存储banner item的数据

eh_launch_pad_items，存储非banner item的数据

理论上两种item它们应该在一张表中，但是由于历史原因，这两种数据还是分开存储了，这也增加了后期处理的复杂性

事实上，这三张表的关联关系也有些复杂，在这里做一个简单的描述，更详细的关于字段的操作，见ORM中的描述

**eh_launch_pad_layouts**
总领全部数据的表

这个表中有很多字段，我们关注以下几个
   * namespace_id 域空间id
   * scene_type   区别登陆者的类型
   * scope_code, scope_id   说明这个layout是用于某个特定scope
   * name       layout的名称，而且一个name对应一个item_location 服务市场ServiceMarketLayout <=> /home， 之后建议 <LayoutDesc>Layout <=> /home/<LayoutDesc>,比如  PmLayout <=> /home/Pm,这样的关联关系来自于 action_data 中对(action_type=2 跳转layout)的定义，

以上的5个字段是选中某个特定layout所必须有的字段，我们称之为 selector，这也引申出了后续前后端交互中，一个重要的selector的参数
   * layout_json 这个字段中，存储了一个json化的字符串，存放多余的数据，数据结构如下：

.. code-block:: javascript

   {
     "versionCode": "2016110101",
     "versionName": "3.0.0",
     "layoutName": "ServiceMarketLayout",
     "displayName": "服务市场",
     "groups": [
       {
         "groupName": "",
         "widget": "Banners",
         "instanceConfig": {
           "itemGroup": "Default"
         },
         "style": "Default",
         "defaultOrder": 1,
         "separatorFlag": 0,
         "separatorHeight": 0
       },
       {
         "groupName": "商家服务",
         "widget": "Navigator",
         "instanceConfig": {
           "itemGroup": "Bizs"
         },
         "style": "Default",
         "defaultOrder": 5,
         "separatorFlag": 0,
         "separatorHeight": 0
       }
     ]
   }

我们主要关注
   * layoutName，标识layout的唯一值
   * displayName，表明layout的名字
   * groups，描述了一个layout中所有widget的数据描述，数组中的每一项对应于一个widget
      * widget 标明了widget的类型，当为Banners的时候，这个widget下的所有item存储在eh_banners表中;否则存储在eh_launch_pad_items表中
      * instanceConfig.itemGroup 这个字段的本义是这样的，一个layout中可能会有多个同一类型的widget，比如有2个Banner，这里就用这个字段来区分两个Banner

由layout > layout_json > groups > widget这样的顺序关系，我们才可以开始检索item数据


**eh_launch_pad_items**
非banner的item数据

其中也有很多字段，我们关注以下的几个:

   * namespace_id 同layout
   * scene_type 同layout
   * scope_code 同layout
   * scope_id 同layout
   * item_location 这里的location，就对应于上面所说的layout_name <=> item_location的对应关系，表明这个item属于哪个layout
   * item_group 这个字段对应上面layout中的instanceConfig.itemGroup，表明此item是属于某个特定的widget的

这6个字段，充当了item的selector,下面的几个字段，记录了关于item本身的数据

   * item_width item所占用的宽度
   * item_height item所占用的高度
   * item_name
   * item_label
   * icon_uri 图片icon的地址
   * action_type, action_data 这是对于一个item非常重要的属性，标明了item的动作类型，可以触发的效果


**eh_banners**
存储banner item,和eh_launch_pad_items的含义是相同的，只不过其用于存储banner item,其中大部分字段是相同的，还有部分字段是含义对应的，但是名称却不同，
我们在后续编码的时候，用一个单独的类来屏蔽这种不同

对应关系： eh_banners中的字段名 <- eh_launch_pad_items的字段名
   * name <- item_name
   * vendor_tag <- item_label
   * poster_path <- icon_uri
   * banner_location <- item_location
   * banner_group <- item_group

相同的字段：
   * action_type
   * action_data
   * namespace_id
   * scene_type
   * scope_code
   * scope_id


通过上面的分析，我们很容易得到这样的数据结构进行前后端的交互

前端通过selector，请求相应的layout,widget,item数据

selector >>>>>

.. code-block:: javascript

   selector: {
     ns: 999992,
     scene: 'pm_admin',
     scope_code: 0,
     scope_id: 0,
     layout: 'ServiceMarketLayout',
   }


后端返回具体的layout,widget,item数据

<<<<<< data

这里的数据结构与layout_json相同，区别在于，将特定widget对应的item数据，作为items数组，成为group widget的一部分

其中的层次关系是非常明显的

.. code-block:: javascript

   data: {
     layoutName: ServiceMarketLayout,
     displayName: 服务市场,
     // layout的其它数据，多余的可扩展
     groups:[
       {
         groupName: '',
         widget: 'Banners',
         instanceConfig: {
           itemGroup: 'GaActions'
         },
         style: 'Default',
         defaultOrder: 1, //数组顺序
         separatorFlag: 1, // 由seperatorHeight是否为0决定
         separatorHeight: 21,
         // widget的其它key-value数据

         items: [
           {
             // 常规item
             item_name: '',
             item_lable: '',
             icon_uri: '',
             item_width: 1,
             item_height: 1,
             action_type: 19,
             action_data: '',
             // item的其它数据
           }
         ]
       }
     ]
   }

这就是之后定义api,包括前端redux store的数据形式来源 :)
