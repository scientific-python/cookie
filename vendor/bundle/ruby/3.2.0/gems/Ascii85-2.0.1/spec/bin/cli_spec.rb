# frozen_string_literal: true

require 'stringio'
require 'tempfile'

require 'minitest/autorun'

# We can't require the executable file because it doesn't 
# have the '.rb' extension, so we have to load it.
unless defined?(CLI)
  load File.join(__dir__, '..','..', 'bin', 'ascii85')
end

describe 'CLI' do
  it 'should recognize the -h and --help options' do
    [%w[-h], %w[--help]].each do |args|
      cli = CLI.new(args)
      assert_equal :help, cli.options[:action]
    end
  end

  it 'should recognize the -V and --version options' do
    [%w[-V], %w[--version]].each do |args|
      cli = CLI.new(args)
      assert_equal :version, cli.options[:action]
    end
  end

  it 'should complain about superfluous arguments' do
    assert_raises(OptionParser::ParseError) do
      CLI.new(%w[foo bar])
    end
  end

  describe 'wrap' do
    it 'should default to wrapping at 80 characters' do
      cli = CLI.new([])
      assert_equal 80, cli.options[:wrap]
    end

    it 'should recognize the -w and --wrap options' do
      [%w[-w 17], %w[--wrap 17]].each do |args|
        cli = CLI.new(args)
        assert_equal 17, cli.options[:wrap]
      end
    end

    it 'should recognize the no-wrapping setting' do
      cli = CLI.new(%w[-w 0])
      assert_equal false, cli.options[:wrap]
    end

    it 'should raise an error if the wrap option is not an integer' do
      assert_raises(OptionParser::ParseError) do
        CLI.new(%w[-w foo])
      end
    end
  end

  describe 'encoding' do
    it 'should encode from STDIN' do
      stdin = StringIO.new('Ruby')
      stdout = StringIO.new

      CLI.new([], stdin: stdin, stdout: stdout).call

      assert_equal '<~;KZGo~>', stdout.string
    end

    it 'should accept "-" as a file name' do
      stdin = StringIO.new('Ruby')
      stdout = StringIO.new

      CLI.new(['-'], stdin: stdin, stdout: stdout).call

      assert_equal '<~;KZGo~>', stdout.string
    end

    it 'should encode a file' do
      begin
        f = Tempfile.create('ascii85_encode')
        f.write('Ruby')
        f.close

        stdout = StringIO.new
        CLI.new([f.path], stdout: stdout).call

        assert_equal '<~;KZGo~>', stdout.string
      ensure
        File.unlink(f.path) 
      end
    end

    it 'should wrap lines' do
      begin
        f = Tempfile.create('ascii85_wrap')
        f.write('a' * 20)
        f.close

        stdout = StringIO.new
        CLI.new([f.path, '-w2'], stdout: stdout).call

        assert stdout.string.lines.all? { |l| l.chomp.length <= 2 }
      ensure
        File.unlink(f.path) 
      end
    end

    it 'should fail when the input file is not found' do
      assert_raises(StandardError) do
        CLI.new(['./foo/bar/baz']).call
      end
    end

    it 'should fail when the input file is not readable' do
      begin
        f = Tempfile.create('ascii85_encode')
        f.chmod(0o000)

        assert_raises(StandardError) do
          CLI.new([f.path]).call
        end
      ensure
        File.unlink(f.path) 
      end
    end
  end

  describe 'decoding' do
    it 'should decode from STDIN' do
      stdin = StringIO.new('<~;KZGo~>')
      stdout = StringIO.new

      CLI.new(['-d'], stdin: stdin, stdout: stdout).call

      assert_equal 'Ruby', stdout.string
    end

    it 'should accept "-" as a file name' do
      stdin = StringIO.new('<~;KZGo~>')
      stdout = StringIO.new

      CLI.new(['-d','-'], stdin: stdin, stdout: stdout).call

      assert_equal 'Ruby', stdout.string
    end

    it 'should decode a file' do
      begin
        f = Tempfile.create('ascii85_decode')
        f.write('<~;KZGo~>')
        f.close

        stdout = StringIO.new
        CLI.new(['-d', f.path], stdout: stdout).call

        assert_equal 'Ruby', stdout.string
      ensure
        File.unlink(f.path) 
      end
    end

    it 'should fail when the input file is not found' do
      assert_raises(StandardError) do
        CLI.new(['-d', './foo/bar/baz']).call
      end
    end

    it 'should fail when the input file is not readable' do
      begin
        f = Tempfile.create('ascii85_decode')
        f.chmod(0o000)

        assert_raises(StandardError) do
          CLI.new(['-d', f.path]).call
        end
      ensure
        File.unlink(f.path) 
      end
    end

    describe 'invalid input' do
      it 'should return the empty string when the input does not have delimiters' do 
        stdin = StringIO.new('No delimiters')
        stdout = StringIO.new

        CLI.new(['-d'], stdin: stdin, stdout: stdout).call

        assert_equal '', stdout.string
      end

      ERROR_CASES = [
        '<~!!y!!~>',
        '<~!!z!!~>',
        '<~s8W-#~>',
        '<~!~>',
      ]

      it 'should raise an error when invalid input is encountered' do
        ERROR_CASES.each do |input|
          stdin = StringIO.new(input)
          stdout = StringIO.new

          assert_raises(Ascii85::DecodingError) do
            CLI.new(['-d'], stdin: stdin, stdout: stdout).call
          end
        end
      end
    end
  end
end