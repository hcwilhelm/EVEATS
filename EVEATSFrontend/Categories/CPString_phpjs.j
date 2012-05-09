/* 
 * More info at: http://phpjs.org
 * http://phpjs.org/functions/index
 *
 * php.js is copyright 2009 Kevin van Zonneveld.
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * Conversion to Objective-J copyright 2009 Philippe Laval
 * Licenced under the same MIT, GPL dual licences.
 */

@import <Foundation/CPObject.j>

@implementation CPString (phpjs)

- (CPString)trim
{
	return [self trimWithCharlist:null];
}

- (CPString)trimWithCharlist:(CPString)charlist
{
    // Strips whitespace from the beginning and end of a string  
    // 
    // version: 812.316
    // discuss at: http://phpjs.org/functions/trim
    // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   improved by: mdsjack (http://www.mdsjack.bo.it)
    // +   improved by: Alexander Ermolaev (http://snippets.dzone.com/user/AlexanderErmolaev)
    // +      input by: Erkekjetter
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +      input by: DxGx
    // +   improved by: Steven Levithan (http://blog.stevenlevithan.com)
    // +    tweaked by: Jack
    // +   bugfixed by: Onno Marsman
    // *     example 1: trim('    Kevin van Zonneveld    ');
    // *     returns 1: 'Kevin van Zonneveld'
    // *     example 2: trim('Hello World', 'Hdle');
    // *     returns 2: 'o Wor'
    // *     example 3: trim(16, 1);
    // *     returns 3: 6
    var whitespace, l = 0, i = 0;
    self += '';
    
    if (!charlist) {
        // default list
        whitespace = " \n\r\t\f\x0b\xa0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u200b\u2028\u2029\u3000";
    } else {
        // preg_quote custom list
        charlist += '';
        whitespace = charlist.replace(/([\[\]\(\)\.\?\/\*\{\}\+\$\^\:])/g, '\$1');
    }
    
    l = self.length;
    for (i = 0; i < l; i++) {
        if (whitespace.indexOf(self.charAt(i)) === -1) {
            self = self.substring(i);
            break;
        }
    }
    
    l = self.length;
    for (i = l - 1; i >= 0; i--) {
        if (whitespace.indexOf(self.charAt(i)) === -1) {
            self = self.substring(0, i + 1);
            break;
        }
    }
    
    return whitespace.indexOf(self.charAt(0)) === -1 ? self : '';
}

- (CPString)rtrim
{
	return [self rtrimWithCharlist:null];
}

- (CPString)rtrimWithCharlist:(CPString)charlist
{
	debugger;
	
    // Removes trailing whitespace  
    // 
    // version: 810.1317
    // discuss at: http://phpjs.org/functions/rtrim
    // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +      input by: Erkekjetter
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   bugfixed by: Onno Marsman
    // *     example 1: rtrim('    Kevin van Zonneveld    ');
    // *     returns 1: '    Kevin van Zonneveld'
    charlist = !charlist ? ' \s\xA0' : (charlist+'').replace(/([\[\]\(\)\.\?\/\*\{\}\+\$\^\:])/g, '\$1');
    var re = new RegExp('[' + charlist + ']+$', 'g');
    return (self+'').replace(re, '');
}

- (CPString)ltrim
{
	return [self ltrimWithCharlist:null];
}

- (CPString)ltrimWithCharlist:(CPString)charlist
{
	debugger;
	
    // Strips whitespace from the beginning of a string  
    // 
    // version: 810.1317
    // discuss at: http://phpjs.org/functions/ltrim
    // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +      input by: Erkekjetter
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   bugfixed by: Onno Marsman
    // *     example 1: ltrim('    Kevin van Zonneveld    ');
    // *     returns 1: 'Kevin van Zonneveld    '
    charlist = !charlist ? ' \s\xA0' : (charlist+'').replace(/([\[\]\(\)\.\?\/\*\{\}\+\$\^\:])/g, '\$1');
    var re = new RegExp('^[' + charlist + ']+', 'g');
    return (self+'').replace(re, '');
}

- (CPString)urlencode
{
    // URL-encodes string 
    //
    // version: 901.1411
    // discuss at: http://phpjs.org/functions/urlencode
    // +   original by: Philip Peterson
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +      input by: AJ
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   improved by: Brett Zamir
    // %          note: info on what encoding functions to use from: http://xkr.us/articles/javascript/encode-compare/
    // *     example 1: urlencode('Kevin van Zonneveld!');
    // *     returns 1: 'Kevin+van+Zonneveld%21'
    // *     example 2: urlencode('http://kevin.vanzonneveld.net/');
    // *     returns 2: 'http%3A%2F%2Fkevin.vanzonneveld.net%2F'
    // *     example 3: urlencode('http://www.google.nl/search?q=php.js&;ie=utf-8&oe=utf-8&aq=t&rls=com.ubuntu:en-US:unofficial&client=firefox-a');
    // *     returns 3: 'http%3A%2F%2Fwww.google.nl%2Fsearch%3Fq%3Dphp.js%26ie%3Dutf-8%26oe%3Dutf-8%26aq%3Dt%26rls%3Dcom.ubuntu%3Aen-US%3Aunofficial%26client%3Dfirefox-a'
                              
    var histogram = {}, tmp_arr = [];
    var ret = self.toString();
     
    var replacer = function(search, replace, str) {
        var tmp_arr = [];
        tmp_arr = str.split(search);
        return tmp_arr.join(replace);
    };
     
    // The histogram is identical to the one in urldecode.
    histogram["'"]   = '%27';
    histogram['(']   = '%28';
    histogram[')']   = '%29';
    histogram['*']   = '%2A';
    histogram['~']   = '%7E';
    histogram['!']   = '%21';
    histogram['%20'] = '+';
     
    // Begin with encodeURIComponent, which most resembles PHP's encoding functions
    ret = encodeURIComponent(ret);
     
    for (search in histogram) {
        replace = histogram[search];
        ret = replacer(search, replace, ret) // Custom replace. No regexing
    }
     
    // Uppercase for full PHP compatibility
    return ret.replace(/(\%([a-z0-9]{2}))/g, function(full, m1, m2) {
        return "%"+m2.toUpperCase();
    });
     
    return ret;
}

@end