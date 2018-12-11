function getDirectory(e) {
    var files = e.target.files;
    var path = files[0].webkitRelativePath;
    var Folder = path.split('/');
    $('').innerHTML = Folder[0];
}




