# frozen_string_literal: true

module SP
  # Sets up a tabs with top switcher bar
  class Tabs < Liquid::Block
    def render(context)
      tab_bar_content = ''
      context['tabs'] = []
      result = super

      context['tabs'].each_with_index do |(label, title), index|
        res = index.zero? ? ' btn-purple' : ''
        tab_bar_content += <<~CONTENT
          <button class="skhep-bar-item #{label}-btn btn m-2#{res}" onclick="openTab('#{label}')">#{title}</button>
        CONTENT
      end

      <<~RETURN
        <div class="skhep-bar d-flex m-2" style="justify-content:center;">
        #{tab_bar_content}
        </div>
        #{result}
      RETURN
    end
  end

  # Sets up tabs without the top switcher bar
  class TabBodies < Liquid::Block
    def render(context)
      context['tabs'] = []
      super
    end
  end

  # This is the content of each tab
  class Tab < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
      @label, @title = markup.strip.split(/ /, 2)
    end

    def render(context)
      raise SyntaxError, "'tab' be in 'tabs' or 'tabbodies'" unless context.key?('tabs')

      res = context['tabs'].empty? ? '' : ' style="display:none;"'
      context['tabs'] << [@label, @title]
      <<~RETURN
        <div class="skhep-tab #{@label}-tab" markdown="1"#{res}>
        #{super}
        </div>
      RETURN
    end
  end
end

Liquid::Template.register_tag('tabs', SP::Tabs)
Liquid::Template.register_tag('tabbodies', SP::TabBodies)
Liquid::Template.register_tag('tab', SP::Tab)
