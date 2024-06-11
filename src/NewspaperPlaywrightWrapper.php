<?php
namespace Twodareis2do\ScrapeNewspaperPlaywright;

use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

/**
 * PHP wrapper for python newspaper3/4k text processor with Playwright support.
 */
class NewspaperPlaywrightWrapper
{
    /**
     * Accepts url string and returns Article object as an associative array.
     * 
     * @param string $url
     * @param boolean $debug
     * 
     * @return array|object
     */
    public function scrape(string $url, $debug = FALSE)
    {
        $command = 'python3';
        $executable = dirname(__FILE__) . '/ArticleScraping.py';

        $commands = [$command, $executable, $url];

        $process = new Process($commands, null, null, null, null);
        $process->run();

        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $json = $process->getOutput();

        if($debug) {
            $this->debug($url, $json);
        }

        // Encode json to associative array
        return json_decode($json, true);
    }

    public function debug(string $url, string $json) {
        $host = parse_url($url, PHP_URL_HOST); 
        // Generate json file.
        $milliseconds = floor(microtime(true) * 1000);
        file_put_contents("/tmp/debug_" . $host . "_" . $milliseconds . ".json", $json);
    }
}
