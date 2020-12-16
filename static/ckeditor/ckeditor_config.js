// Page Create

if(document.querySelector('#id_content' ))
{
    ClassicEditor.create( document.querySelector('#id_content' ), {
        language : 'en',
        toolbar: [ 'heading', '|', 'bold', 'italic', '|', 'link','blockQuote','codeBlock', 
        '|','numberedList','bulletedList','indent','outdent','|','undo','redo'],
        codeBlock: {
            languages: [{ language: 'plaintext', label: 'Plain Code', class: '' }]
    }
    }).then( id_content => {
        window.id_content = id_content;
    }).catch( err => {    
        console.error( err.stack );
    } );

}
else if (document.querySelector('#id_answer_content' ))
{
    
    // Comment
    ClassicEditor.create( document.querySelector('#id_answer_content' ), {
        language : 'en',
        toolbar: [ 'heading', '|', 'bold', 'italic', '|', 'link','codeBlock', 
        '|','numberedList','bulletedList','indent','outdent','|','undo','redo'],
        codeBlock: {
            languages: [{ language: 'plaintext', label: 'Plain Code', class: '' }]
    }
    }).then( id_answer_content => {
        window.id_answer_content = id_answer_content;
    }).catch( err => {    
        console.error( err.stack );
    } );

    // Comment Edit
    ClassicEditor.create( document.querySelector('#id_comment_content_edit' ), {
        language : 'en',
        toolbar: [ 'heading', '|', 'bold', 'italic', '|', 'link','codeBlock', 
        '|','numberedList','bulletedList','indent','outdent','|','undo','redo'],
        codeBlock: {
            languages: [{ language: 'plaintext', label: 'Plain Code', class: '' }]
    }
    }).then( id_comment_content_edit => {
        window.id_comment_content_edit = id_comment_content_edit;
    }).catch( err => {    
        console.error( err.stack );
    } );

}





