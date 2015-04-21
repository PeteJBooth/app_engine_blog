requirejs.config({
    'shim': {
        'ckeditor-jquery':{
            deps:['jquery','ckeditor-core']
        }
    },
    "baseUrl": "/static/js/lib",
    "paths": {
      "modules": "../modules",
      "jquery": "//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min",
      "ckeditor-core": "ckeditor/ckeditor",
      "ckeditor-jquery": "ckeditor/adapters/jquery"
    }
});

requirejs(["modules/main"]);