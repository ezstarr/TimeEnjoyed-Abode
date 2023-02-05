/**
 * @license Copyright (c) 2003-2022, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    config.toolbarGroups = [
		{ name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
		{ name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
		{ name: 'forms', groups: [ 'forms' ] },
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
		{ name: 'links', groups: [ 'links' ] },
		{ name: 'insert', groups: [ 'insert' ] },
		{ name: 'document', groups: [ 'document', 'doctools', 'mode' ] },
		'/',
		{ name: 'styles', groups: [ 'styles' ] },
		{ name: 'colors', groups: [ 'colors' ] },
		{ name: 'tools', groups: [ 'tools' ] },
		{ name: 'others', groups: [ 'others' ] },
		{ name: 'about', groups: [ 'about' ] }
	];

	config.removeButtons = 'Replace,Find,SelectAll,Scayt,Form,Checkbox,Radio,Select,Button,ImageButton,HiddenField,Textarea,TextField,CreateDiv,JustifyCenter,JustifyBlock,JustifyRight,BidiLtr,BidiRtl,Language,Flash,PageBreak,Iframe,Save,NewPage,Preview,Print,Templates,Cut,Copy,Undo,Redo,Paste,PasteText,PasteFromWord,About';
    config.extraPlugins = 'codesnippet';


};

// Create a new plugin which registers a custom code highlighter
// based on customEngine in order to replace the one that comes
// with the Code Snippet plugin.
CKEDITOR.plugins.add( 'myCustomHighlighter', {
    afterInit: function( editor ) {
        // Create a new instance of the highlighter.
        var myHighlighter = new CKEDITOR.plugins.codesnippet.highlighter( {
            init: function( ready ) {
                // Asynchronous code to load resources and libraries for customEngine.
                customEngine.loadResources( function() {
                    // Let the editor know that everything is ready.
                    ready();
                } );
            },
            highlighter: function( code, language, callback ) {
                // Let the customEngine highlight the code.
                customEngine.highlight( code, language, function() {
                    callback( highlightedCode );
                } );
            }
        } );

        // Check how it performs.
        myHighlighter.highlight( 'foo()', 'javascript', function( highlightedCode ) {
            console.log( highlightedCode ); // -> <span class="pretty">foo()</span>
        } );

        // From now on, myHighlighter will be used as a Code Snippet
        // highlighter, overwriting the default engine.
        editor.plugins.codesnippet.setHighlighter( myHighlighter );
    }
} );