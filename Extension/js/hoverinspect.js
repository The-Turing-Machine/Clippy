var injected = injected || (function() {

    var user = prompt("Enter Your Username", "Harry Potter");
    var data, jsonArray, url;
    var lis = [],
        jsonlist = [];
    var i = 0;

    var Inspector = function() {
        this.highlight = this.highlight.bind(this);
        this.log = this.log.bind(this);
        this.codeOutput = this.codeOutput.bind(this);
        this.layout = this.layout.bind(this);
        this.handleResize = this.handleResize.bind(this);

        this.$target = document.body;
        this.$cacheEl = document.body;
        this.$cacheElMain = document.body;

        this.serializer = new XMLSerializer();
        this.forbidden = [this.$cacheEl, document.body, document.documentElement];
    };

    Inspector.prototype = {

        getNodes: function() {
            var path = chrome.extension.getURL("static/template.html");

            var xmlhttp = new XMLHttpRequest();

            xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                    this.template = xmlhttp.responseText;
                    this.createNodes();
                    this.registerEvents();
                }
            }.bind(this);

            xmlhttp.open("GET", path, true);
            xmlhttp.send();
        },

        createNodes: function() {

            this.$host = document.createElement('div');
            this.$host.className = 'tl-host';
            this.$host.style.cssText = 'all: initial;';


            var shadow = this.$host.createShadowRoot();
            document.body.appendChild(this.$host);

            var templateMarkup = document.createElement("div");
            templateMarkup.innerHTML = this.template;
            shadow.innerHTML = templateMarkup.querySelector('template').innerHTML;

            this.$wrap = shadow.querySelector('.tl-wrap');
            this.$code = shadow.querySelector('.tl-code');

            this.$canvas = shadow.querySelector('#tl-canvas');
            this.c = this.$canvas.getContext('2d');
            this.width = this.$canvas.width = window.innerWidth;
            this.height = this.$canvas.height = window.innerHeight;

            this.highlight();
        },

        registerEvents: function() {
            document.addEventListener('mousemove', this.log);
            document.addEventListener('scroll', this.layout);

            window.addEventListener('resize', function() {
                this.handleResize();
                this.layout();
            }.bind(this));
        },

        log: function(e) {
            this.$target = e.target;

            // check if element cached
            if (this.forbidden.indexOf(this.$target) !== -1) return;

            this.stringified = this.serializer.serializeToString(this.$target);

            data = this.$target;
            this.codeOutput();

            this.$cacheEl = this.$target;
            this.layout();

        },

        codeOutput: function() {
            if (this.$cacheElMain === this.$target) return;
            this.$cacheElMain = this.$target;
            var fullCode = this.stringified
                .slice(0, this.stringified.indexOf('>') + 1)
                .replace(/ xmlns="[^"]*"/, '');


            document.addEventListener('click', handle);

            function handle() {
                handler1();
                //handler2();
            }

            function handler1(e) {
                //if($(this).)
                if (event.handled !== true) {
                    lis.push(data);
                    //document.getElementById('absSlide').cssText="right:0";
                    if (i == 0) {
                        url = lis[0].baseURI;
                    }
                    jsonlist.push(lis[i].innerText);
                    i++;
                    //alert('Exec!');
                    jsonArray = JSON.parse(JSON.stringify(jsonlist));
                    console.log(url);
                    console.log(user);
                    console.log(jsonArray);

                    event.handled = true;

                }
                return false;
            }

            function handler2(e) {
                $.ajax({
                    type: 'POST',
                    url: 'https://appclippy.herokuapp.com/receive',
                    data: JSON.stringify({ "userid": user, "url": url, "data": jsonArray }), // or JSON.stringify ({name: 'jonas'}),
                    contentType: "application/json",
                    dataType: 'json'
                });
            }

            this.$code.innerText = fullCode; // set full element code
            this.highlight(); // highlight element

        },

        // redraw overlay
        layout: function() {
            var box, computedStyle, rect;
            var c = this.c;

            rect = this.$target.getBoundingClientRect();
            computedStyle = window.getComputedStyle(this.$target);
            box = {
                width: rect.width,
                height: rect.height,
                top: rect.top,
                left: rect.left,
                margin: {
                    top: computedStyle.marginTop,
                    right: computedStyle.marginRight,
                    bottom: computedStyle.marginBottom,
                    left: computedStyle.marginLeft
                },
                padding: {
                    top: computedStyle.paddingTop,
                    right: computedStyle.paddingRight,
                    bottom: computedStyle.paddingBottom,
                    left: computedStyle.paddingLeft
                }
            };

            // pluck negatives
            ['margin', 'padding'].forEach(function(property) {
                for (var el in box[property]) {
                    var val = parseInt(box[property][el], 10);
                    box[property][el] = Math.max(0, val);
                }
            });

            c.clearRect(0, 0, this.width, this.height);

            box.left = Math.floor(box.left) + 1.5;
            box.width = Math.floor(box.width) - 1;

            var x, y, width, height;

            //margin
            // x = box.left + box.margin.left;
            // y = box.top + box.margin.top;
            // width = box.width + box.margin.left + box.margin.right + 50;
            // height = box.height + box.margin.top + box.margin.bottom + 50;

            // c.fillStyle = 'rgba(255, 220, 232, 0.5)';
            // c.fillRect(x, y, width, height);

            // padding
            x = box.left + 2;
            y = box.top + 3;
            width = box.width + 3;
            height = box.height + 3;

            c.fillStyle = 'rgba(0, 77, 64, 0.8)';
            //c.clearRect(x, y, width, height);
            c.fillRect(x, y, width, height);

            // content
            x = box.left;
            y = box.top + 2;
            width = box.width + 2;
            height = box.height + 2;

            c.fillStyle = 'rgba(0, 150, 136, 0.4)';
            c.clearRect(x, y, width, height);
            c.fillRect(x, y, width, height);

        },

        handleResize: function() {
            this.width = this.$canvas.width = window.innerWidth;
            this.height = this.$canvas.height = window.innerHeight;
        },

        // code highlighting
        highlight: function() {
            Prism.highlightElement(this.$code);

        },

        activate: function() {
            this.getNodes();

        },

        deactivate: function() {

            this.$wrap.classList.add('-out');
            document.removeEventListener('mousemove', this.log);
            setTimeout(function() {
                document.body.removeChild(this.$host);
            }.bind(this), 600);
        }

    };

    var hi = new Inspector();


    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        if (request.action === 'activate') {
            return hi.activate();
        } else {
            lis = [];
            jsonlist = [];
            return hi.deactivate();
        }
    });

    return true;
})();
