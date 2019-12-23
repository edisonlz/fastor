/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	var __weex_template__ = __webpack_require__(1)
	var __weex_style__ = __webpack_require__(2)
	var __weex_script__ = __webpack_require__(3)

	__weex_define__('@weex-component/9a105f9ec0af5f83bce33cbb1bd9580b', [], function(__weex_require__, __weex_exports__, __weex_module__) {

	    __weex_script__(__weex_module__, __weex_exports__, __weex_require__)
	    if (__weex_exports__.__esModule && __weex_exports__.default) {
	      __weex_module__.exports = __weex_exports__.default
	    }

	    __weex_module__.exports.template = __weex_template__

	    __weex_module__.exports.style = __weex_style__

	})

	__weex_bootstrap__('@weex-component/9a105f9ec0af5f83bce33cbb1bd9580b',undefined,undefined)

/***/ },
/* 1 */
/***/ function(module, exports) {

	module.exports = {
	  "type": "div",
	  "children": [
	    {
	      "type": "text",
	      "attr": {
	        "value": "轮播图1"
	      }
	    },
	    {
	      "type": "wxc-panel",
	      "attr": {
	        "title": "auto-play",
	        "type": "primary"
	      },
	      "children": [
	        {
	          "type": "slider",
	          "classList": [
	            "slider"
	          ],
	          "children": [
	            {
	              "type": "indicator",
	              "classList": [
	                "indicator"
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716476_3fc77204b12a6ec66bc4492faae9e257"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "周末放映室"
	                  }
	                }
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716526_156005c5baf40ff51a327f1c34f2975b"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "来自鬼畜区的魔性歌声"
	                  }
	                }
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716561_799bad5a3b514f096e69bbc4a7896cd9"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "生存游戏安利"
	                  }
	                }
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716590_d0096ec6c83575373e3a21d129ff8fef"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "diy手作狂人"
	                  }
	                }
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716603_032b2cc936860b03048302d991c3498f"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "pink up 2"
	                  }
	                }
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716634_18e2999891374a475d0687ca9f989d83"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "懒人饿不死"
	                  }
	                }
	              ]
	            },
	            {
	              "type": "div",
	              "classList": [
	                "slider-page"
	              ],
	              "children": [
	                {
	                  "type": "image",
	                  "classList": [
	                    "slider-item"
	                  ],
	                  "attr": {
	                    "src": "http://picture01-10022394.image.myqcloud.com/1463716715_fe5df232cafa4c4e0f1a0294418e5660"
	                  }
	                },
	                {
	                  "type": "text",
	                  "classList": [
	                    "slider-title"
	                  ],
	                  "attr": {
	                    "value": "国产很强势"
	                  }
	                }
	              ]
	            }
	          ]
	        }
	      ]
	    }
	  ]
	}

/***/ },
/* 2 */
/***/ function(module, exports) {

	module.exports = {
	  "slider": {
	    "flexDirection": "row",
	    "width": 750,
	    "height": 360
	  },
	  "indicator": {
	    "position": "absolute",
	    "itemSize": 10,
	    "width": 750,
	    "height": 420,
	    "top": 60,
	    "left": -320,
	    "margin": 10,
	    "itemColor": "#dddddd",
	    "itemSelectedColor": "blue"
	  },
	  "slider-page": {
	    "flexDirection": "row",
	    "justifyContent": "space-between",
	    "width": 750,
	    "height": 420
	  },
	  "slider-item": {
	    "width": 750,
	    "height": 400
	  },
	  "slider-title": {
	    "position": "absolute",
	    "top": 300,
	    "left": 20,
	    "color": "#FFFFFF"
	  }
	}

/***/ },
/* 3 */
/***/ function(module, exports) {

	module.exports = function(module, exports, __weex_require__){'use strict';

	module.exports = {
	  data: function () {return {
	    page: '精选轮播图测试',
	    videos: [{
	      id: 1,
	      img: 'http://g1.ykimg.com/0515000058474E0867BC3D0D62007E54',
	      title: '<国产大英雄2>校园宫心计'
	    }, {
	      id: 2,
	      img: 'http://g1.ykimg.com/0515000058474E8967BC3D2F930400B6',
	      title: '[非诚勿扰]"照骗女"美照惊全场'
	    }, {
	      id: 3,
	      img: 'http://g1.ykimg.com/0515000058474EFF67BC3D2F3700ECFF',
	      title: '[维密]超模玩转"捆绑"炫裸臀'
	    }]
	  }},
	  methods: {}
	};}
	/* generated by weex-loader */


/***/ }
/******/ ]);