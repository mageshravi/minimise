var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');

var uglify = require('gulp-uglify');

var scssFiles = './scss/**/*.scss';
var cssDir = './static/css';

var sass_options = {
    errLogToConsole: true,
    outputStyle: 'expanded'
};

var jsFiles = './scripts/**/*.js';
var jsDir = './static/js';

gulp.task('sass', function () {
  return gulp.src(scssFiles)
         .pipe(sourcemaps.init())
         .pipe(sass(sass_options).on('error', sass.logError))
         .pipe(sourcemaps.write())
         .pipe(autoprefixer())
         .pipe(gulp.dest(cssDir));
});

gulp.task('compress-js', function () {
  return gulp.src(jsFiles)
         .pipe(uglify())
         .pipe(gulp.dest(jsDir));
});

gulp.task('watch', function () {
  gulp.watch(scssFiles, ['sass']).on('change', function (event) {
    console.log('SCSS: ' + event.path + ' was ' + event.type + ', running tasks...');
  });

  gulp.watch(jsFiles, ['compress-js']).on('change', function (event) {
    console.log('JS: ' + event.path + ' was ' + event.type + ', running tasks...');
  });
});

gulp.task('default', ['saas', 'compress-js', 'watch']);