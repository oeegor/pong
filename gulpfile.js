var browserify = require('browserify');
var gulp = require('gulp');
var gutil = require('gulp-util');
var nib = require('nib');
var notify = require("gulp-notify");
var reactify = require('reactify');
var source = require('vinyl-source-stream');
var stylus = require('gulp-stylus');
var uglify = require('gulp-uglify');
var watchify = require('watchify');

var scriptsDir = './static';
var buildDir = './dist';


var paths = {
  'stylus': ['static/chrn/styl/**/*.styl'],
};


// Based on: http://blog.avisi.nl/2014/04/25/how-to-keep-a-fast-build-with-browserify-and-reactjs/
function buildScript(file, watch) {
  var props = watchify.args;
  props.entries = [scriptsDir + '/' + file];
  props.debug = true;

  var bundler = watch ? watchify(browserify(props)) : browserify(props);

  bundler.transform(reactify);
  function rebundle() {
    var stream = bundler.bundle();
    return stream.on('error', notify.onError({
        title: "Compile Error",
        message: "<%= error.message %>"
      }))
      .pipe(source(file))
      .pipe(gulp.dest(buildDir + '/'));
  }
  bundler.on('update', function() {
    rebundle();
    gutil.log('Rebundle...');
  });
  return rebundle();
}


gulp.task('build', ['css'], function() {
  return buildScript('chrn/app.jsx', false);
});

gulp.task('css', function() {
  return gulp.src(['static/chrn/styl/main.styl'])
    .pipe(stylus({use:[nib()]}))
    .pipe(gulp.dest(buildDir + '/chrn/'));
});

gulp.task('watch', function() {
  gulp.watch(paths.stylus, ['css']);
});

gulp.task('compress', ['build'], function() {
  return gulp.src(buildDir + '/chrn/app.jsx')
    .pipe(uglify())
    .pipe(gulp.dest(buildDir + '/chrn/'));
});

gulp.task('prod-env', function() {
  return process.env.NODE_ENV = 'production'
});

gulp.task('production', ['prod-env', 'compress']);

gulp.task('default', ['build', 'watch'], function() {
  return buildScript('chrn/app.jsx', true);
});
